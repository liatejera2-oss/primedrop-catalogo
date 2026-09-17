from pathlib import Path

# Patch public catalog
index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
orig_index = index

old_load = '''      renderAllSizeRows();
      renderAllStatusTags();
      renderAllPrices();
      renderAllPurchaseButtons();
      migrateUpcomingCards();
    }
'''
new_load = '''      renderAllSizeRows();
      renderAllStatusTags();
      renderAllPrices();
      renderAllPurchaseButtons();
      await syncUpcomingPublicationState();
      migrateUpcomingCards();
    }
'''
if old_load not in index:
    raise SystemExit('index loadCatalog block not found')
index = index.replace(old_load, new_load, 1)

anchor = '''    // Si una prenda de "Próximos drops" ya fue publicada (tiene fila
'''
sync_fn = '''    async function syncUpcomingPublicationState() {
      const { data, error } = await client.rpc('get_published_product_states');
      if (error) {
        console.warn('[Prime Drop] No se pudo consultar el historial de publicación:', error.message);
        return;
      }

      const states = new Map((data || []).map(row => [row.slug, row]));
      document.querySelectorAll('.upcoming-card').forEach(card => {
        const tag = card.querySelector('[data-stock-status]');
        if (!tag) return;
        const state = states.get(tag.dataset.stockStatus);
        if (!state || state.published_once !== true) return;

        // Si ya se publicó alguna vez pero hoy está oculto, no debe volver a
        // aparecer en Próximos Drops. Si está activo, migrateUpcomingCards()
        // lo moverá inmediatamente al catálogo principal.
        if (state.active !== true) card.remove();
      });

      const upcomingSection = document.getElementById('upcomingSection');
      const upcomingSectionHead = document.getElementById('upcomingSectionHead');
      if (upcomingSection && !upcomingSection.querySelector('.upcoming-card')) {
        upcomingSection.style.display = 'none';
        if (upcomingSectionHead) upcomingSectionHead.style.display = 'none';
      }
    }

'''
if anchor not in index:
    raise SystemExit('index migration anchor not found')
index = index.replace(anchor, sync_fn + anchor, 1)

if index == orig_index:
    raise SystemExit('No index changes made')
index_path.write_text(index, encoding='utf-8')

# Patch private panel
panel_path = Path('panel-privado.html')
panel = panel_path.read_text(encoding='utf-8')
orig_panel = panel

old_block = '''    const productPayload = {
      slug, name, category: 'T-shirt', sale_mode: 'in_stock',
      regular_price: isNaN(price) ? 0 : price,
      active: !!publishBtn
    };
    if (publishBtn) productPayload.published_once = true;

    const { data: prod, error: pErr } = await client
      .from('products')
      .upsert(productPayload, { onConflict: 'slug' })
      .select()
      .single();

    if (pErr) {
      btn.disabled = false;
      showMsg(msgEl, (publishBtn ? 'Error publicando: ' : 'Error guardando: ') + pErr.message, 'error');
      return;
    }

    const variantRows = SIZE_ORDER.map(size => ({ product_id: prod.id, size, stock_on_hand: stocks[size] || 0 }));
    const { error: vErr } = await client.from('product_variants').upsert(variantRows, { onConflict: 'product_id,size' });

    btn.disabled = false;
    if (vErr) { showMsg(msgEl, 'Error guardando tallas: ' + vErr.message, 'error'); return; }

    if (publishBtn) {
      showMsg(msgEl, `"${name}" ya está publicado — aparecerá como Disponible en el catálogo y ahora se maneja desde "Inventario".`, 'ok');
      viewLoaded.inventario = false; // fuerza recarga de Inventario la próxima vez que se visite esa pestaña
    } else {
      showMsg(msgEl, `"${name}" se guardó como borrador — sigue sin publicarse ni afectar el catálogo.`, 'ok');
    }
    loadUpcoming();
'''
new_block = '''    if (publishBtn) {
      // Publicar debe ser una sola operación atómica: producto + variantes +
      // active=true + published_once=true. Así evitamos estados parciales donde
      // la tarjeta desaparece de Próximos Drops pero todavía no entra al catálogo.
      const { data, error } = await client.rpc('publish_upcoming_product', {
        p_slug: slug,
        p_name: name,
        p_regular_price: price,
        p_stocks: stocks
      });

      btn.disabled = false;
      if (error) {
        showMsg(msgEl, 'Error publicando: ' + error.message, 'error');
        return;
      }

      const published = Array.isArray(data) ? data[0] : data;
      if (!published || published.active !== true || published.published_once !== true) {
        showMsg(msgEl, 'La publicación no quedó confirmada. Actualiza e intenta nuevamente.', 'error');
        return;
      }

      showMsg(msgEl, `"${name}" ya está publicado — salió de Próximos drops y ahora aparece en el catálogo disponible.`, 'ok');
      viewLoaded.inventario = false;
      await loadUpcoming();
      return;
    }

    // Guardar continúa siendo un borrador no publicado.
    const productPayload = {
      slug, name, category: 'Jersey', sale_mode: 'in_stock',
      regular_price: isNaN(price) ? 0 : price,
      active: false,
      published_once: false
    };

    const { data: prod, error: pErr } = await client
      .from('products')
      .upsert(productPayload, { onConflict: 'slug' })
      .select()
      .single();

    if (pErr) {
      btn.disabled = false;
      showMsg(msgEl, 'Error guardando: ' + pErr.message, 'error');
      return;
    }

    const variantRows = SIZE_ORDER.map(size => ({ product_id: prod.id, size, stock_on_hand: stocks[size] || 0 }));
    const { error: vErr } = await client.from('product_variants').upsert(variantRows, { onConflict: 'product_id,size' });

    btn.disabled = false;
    if (vErr) { showMsg(msgEl, 'Error guardando tallas: ' + vErr.message, 'error'); return; }

    showMsg(msgEl, `"${name}" se guardó como borrador — sigue sin publicarse ni afectar el catálogo.`, 'ok');
    await loadUpcoming();
'''
if old_block not in panel:
    raise SystemExit('panel publish block not found')
panel = panel.replace(old_block, new_block, 1)

if panel == orig_panel:
    raise SystemExit('No panel changes made')
panel_path.write_text(panel, encoding='utf-8')

# Validation
for needle in [
    "await syncUpcomingPublicationState();",
    "client.rpc('get_published_product_states')",
    "client.rpc('publish_upcoming_product'",
    "published.active !== true",
    "published.published_once !== true"
]:
    if needle not in index + panel:
        raise SystemExit(f'Missing expected change: {needle}')
