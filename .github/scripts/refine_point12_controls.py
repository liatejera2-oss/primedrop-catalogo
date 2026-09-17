from pathlib import Path

panel_path = Path('panel-privado.html')
index_path = Path('index.html')
panel = panel_path.read_text(encoding='utf-8')
index = index_path.read_text(encoding='utf-8')


def rep(text, old, new, label, count=1):
    if old not in text:
        raise SystemExit(f'{label}: anchor not found')
    return text.replace(old, new, count)

# ------------------------------------------------------------------
# PANEL — visual system, finance summary, expenses placeholder
# ------------------------------------------------------------------
css_anchor = "  .table-scroll button { padding:6px 11px; }\n"
css_extra = r'''  .table-scroll button { padding:6px 11px; }
  .wrap { width:min(1180px, 100%); }
  button.secondary { background:transparent; }
  button.danger, button.danger-ghost { background:transparent; color:var(--accent); border:1px solid #E8B8BC; }
  button.danger:hover, button.danger-ghost:hover { background:var(--panel-red-soft); color:var(--accent); }
  .finance-summary { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-bottom:20px; }
  .finance-card { background:#fff; border:1px solid var(--panel-line); border-radius:14px; padding:16px; }
  .finance-card span { display:block; color:var(--ink-soft); font-size:11px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; margin-bottom:7px; }
  .finance-card strong { display:block; font-size:22px; letter-spacing:-.025em; }
  .finance-card small { display:block; margin-top:5px; color:var(--ink-soft); font-size:11.5px; line-height:1.35; }
  .finance-note { grid-column:1/-1; color:var(--ink-soft); font-size:11.5px; padding:0 2px; }
  .money-cell { min-width:112px; }
  .money-cell strong { display:block; font-size:13px; }
  .money-cell span, .money-cell small { color:var(--ink-soft); font-size:11.5px; }
  .money-progress { height:3px; background:#ECECE9; border-radius:999px; overflow:hidden; margin:6px 0 4px; }
  .money-progress i { display:block; height:100%; background:var(--ink); border-radius:999px; }
  input.product-name-input, input.upcoming-name-input { min-width:190px; margin:0; font-size:13px; }
  input.product-name-input { width:210px; }
  input.upcoming-name-input { width:280px; }
  .placeholder-card { min-height:220px; display:flex; flex-direction:column; justify-content:center; align-items:flex-start; }
  .placeholder-badge { display:inline-block; padding:5px 10px; border:1px solid var(--panel-line); border-radius:999px; color:var(--ink-soft); font-size:11.5px; font-weight:700; }
  .upcoming-scroll table { min-width:1020px; }
  @media (max-width: 900px) {
    .finance-summary { grid-template-columns:repeat(2,minmax(0,1fr)); }
  }
'''
panel = rep(panel, css_anchor, css_extra, 'panel css')

panel = rep(panel,
'''      <button class="view-tab-btn" data-view="proximos">Próximos drops</button>\n    </div>''',
'''      <button class="view-tab-btn" data-view="proximos">Próximos drops</button>\n      <button class="view-tab-btn" data-view="gastos">Gastos Operativos</button>\n    </div>''',
'nav gastos')

search_end = '''        <div id="searchResult" style="margin-top:14px;"></div>\n      </div>\n\n      <div class="card">'''
finance_html = '''        <div id="searchResult" style="margin-top:14px;"></div>\n      </div>\n\n      <div class="finance-summary" id="financialSummary" aria-label="Resumen financiero básico">\n        <div class="finance-card"><span>Cobrado confirmado</span><strong id="summaryCollected">$0.00</strong><small>Abonos y pagos confirmados.</small></div>\n        <div class="finance-card"><span>Por cobrar</span><strong id="summaryReceivable">$0.00</strong><small>Solicitudes pendientes + saldo de reservas.</small></div>\n        <div class="finance-card"><span>En reservas</span><strong id="summaryReserved">$0.00</strong><small id="summaryReservedCount">0 reservas activas.</small></div>\n        <div class="finance-card"><span>Ventas completadas</span><strong id="summaryPaidSales">$0.00</strong><small id="summaryPaidCount">0 ventas pagadas.</small></div>\n        <div class="finance-note">Resumen operativo básico. No incluye solicitudes canceladas, devoluciones ni gastos.</div>\n      </div>\n\n      <div class="card">'''
panel = rep(panel, search_end, finance_html, 'finance summary html')

panel = rep(panel,
'''          <summary>Cómo funciona una reserva con abono 50%</summary>\n          <div class="details-body">La solicitud no aparta stock mientras esté Pendiente. Al confirmar el abono pasa a Reservada y el stock se descuenta una sola vez. Al completar el saldo pasa a Pagada sin descontar nuevamente. Cancelar una reserva libera el stock; cualquier devolución de dinero se gestiona manualmente. Las reservas confirmadas no vencen automáticamente.</div>''',
'''          <summary>Reservas con abono</summary>\n          <div class="details-body">El stock se aparta cuando confirmas el 50%. Al recibir el saldo, la reserva pasa a Pagada. Si cancelas, el stock se libera.</div>''',
'simplify reservation copy')

panel = rep(panel, '<tr><th>Código</th><th>Total</th><th>Cobrado / saldo</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>', '<tr><th>Código</th><th>Total</th><th>Cobrado / por cobrar</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>', 'orders money header')

# Insert Gastos Operativos placeholder after Próximos view.
insert_anchor = '''      </details>\n    </div>\n  </div>\n</div>\n\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>'''
insert_repl = '''      </details>\n    </div>\n\n    <div id="viewGastos" class="view-section hidden">\n      <div class="card placeholder-card">\n        <span class="placeholder-badge">Módulo preparado</span>\n        <h2 style="margin-top:14px;">Gastos Operativos</h2>\n        <p class="section-intro" style="margin-bottom:0;">Aquí centralizaremos costos de proveedor, shipping, carga marítima o aérea, publicidad y otros gastos operativos. La estructura financiera se configurará en el siguiente ajuste.</p>\n      </div>\n    </div>\n  </div>\n</div>\n\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>'''
panel = rep(panel, insert_anchor, insert_repl, 'gastos section')

# Helpers: extended colors, attribute escaping, better payment cell.
panel = rep(panel,
'''  function colorHexForName(name) {\n    const key = String(name || '').trim().toLowerCase();\n    const known = {\n      'burgundy': '#7B1E3A',\n      'berenjena': '#5A2B55',\n      'azul marino': '#19324F'\n    };\n    return known[key] || '#D9D9D6';\n  }''',
'''  function colorHexForName(name) {\n    const key = String(name || '').trim().toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');\n    const known = {\n      'burgundy': '#7B1E3A', 'berenjena': '#5A2B55', 'azul marino': '#19324F',\n      'rojo': '#C62828', 'red': '#C62828', 'negro': '#202020', 'black': '#202020',\n      'blanco': '#F7F7F5', 'white': '#F7F7F5', 'crema': '#E8DDC5', 'beige': '#D8C7A6',\n      'azul': '#2F5DA8', 'celeste': '#77BDE8', 'verde': '#3E7B55', 'green': '#3E7B55',\n      'amarillo': '#E4B93F', 'naranja': '#D9772B', 'rosa': '#D978A0', 'rosado': '#D978A0',\n      'morado': '#6D4A8E', 'violeta': '#6D4A8E', 'gris': '#8A8F98', 'gray': '#8A8F98',\n      'marron': '#795548', 'cafe': '#795548'\n    };\n    return known[key] || '#D9D9D6';\n  }\n\n  function escapeAttr(value) {\n    return String(value ?? '').replace(/&/g, '&amp;').replace(/\"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');\n  }''',
'panel color helper')

panel = rep(panel,
'''  function paymentProgressHtml(order) {\n    const total = Number(order.total_reference || 0);\n    const paid = Number(order.amount_paid || 0);\n    const balance = Math.max(0, total - paid);\n    return `<span>${moneyFmt(paid)} cobrado</span><br><span style="color:var(--ink-soft);">${moneyFmt(balance)} saldo</span>`;\n  }''',
'''  function paymentProgressHtml(order) {\n    const total = Number(order.total_reference || 0);\n    const paid = Number(order.amount_paid || 0);\n    const balance = Math.max(0, total - paid);\n    const pct = total > 0 ? Math.min(100, Math.max(0, (paid / total) * 100)) : 0;\n    return `<div class="money-cell"><strong>${moneyFmt(paid)} cobrado</strong><div class="money-progress"><i style="width:${pct}%"></i></div><small>${moneyFmt(balance)} por cobrar</small></div>`;\n  }''',
'payment progress')

# Load finance summary and add gastos view.
panel = rep(panel, "    loadOrders('pending');\n", "    loadOrders('pending');\n    loadFinancialSummary();\n", 'session finance load')
panel = rep(panel,
'''  const viewSections = {\n    solicitudes: document.getElementById('viewSolicitudes'),\n    inventario: document.getElementById('viewInventario'),\n    proximos: document.getElementById('viewProximos')\n  };\n  const viewLoaded = { solicitudes: true, inventario: false, proximos: false };''',
'''  const viewSections = {\n    solicitudes: document.getElementById('viewSolicitudes'),\n    inventario: document.getElementById('viewInventario'),\n    proximos: document.getElementById('viewProximos'),\n    gastos: document.getElementById('viewGastos')\n  };\n  const viewLoaded = { solicitudes: true, inventario: false, proximos: false, gastos: true };''',
'view sections gastos')
panel = rep(panel, "    if (currentView === 'solicitudes') loadOrders(activeStatus);\n", "    if (currentView === 'solicitudes') { loadOrders(activeStatus); loadFinancialSummary(); }\n", 'refresh finance')

# Financial summary function.
orders_marker = "  async function loadOrders(status) {\n"
finance_fn = '''  async function loadFinancialSummary() {\n    const { data, error } = await client\n      .from('orders')\n      .select('status, total_reference, amount_paid');\n    if (error) {\n      console.error('[Prime Drop] Error cargando resumen financiero:', error.message);\n      return;\n    }\n\n    const active = (data || []).filter(o => ['pending', 'reserved', 'paid'].includes(o.status));\n    const collected = active.reduce((sum, o) => sum + Number(o.amount_paid || 0), 0);\n    const receivable = active\n      .filter(o => o.status === 'pending' || o.status === 'reserved')\n      .reduce((sum, o) => sum + Math.max(0, Number(o.total_reference || 0) - Number(o.amount_paid || 0)), 0);\n    const reserved = active.filter(o => o.status === 'reserved');\n    const reservedValue = reserved.reduce((sum, o) => sum + Number(o.amount_paid || 0), 0);\n    const paid = active.filter(o => o.status === 'paid');\n    const paidSales = paid.reduce((sum, o) => sum + Number(o.total_reference || 0), 0);\n\n    document.getElementById('summaryCollected').textContent = moneyFmt(collected);\n    document.getElementById('summaryReceivable').textContent = moneyFmt(receivable);\n    document.getElementById('summaryReserved').textContent = moneyFmt(reservedValue);\n    document.getElementById('summaryReservedCount').textContent = `${reserved.length} reserva${reserved.length === 1 ? '' : 's'} activa${reserved.length === 1 ? '' : 's'}.`;\n    document.getElementById('summaryPaidSales').textContent = moneyFmt(paidSales);\n    document.getElementById('summaryPaidCount').textContent = `${paid.length} venta${paid.length === 1 ? '' : 's'} pagada${paid.length === 1 ? '' : 's'}.`;\n  }\n\n'''
panel = rep(panel, orders_marker, finance_fn + orders_marker, 'finance function')

# Refresh finance after state changes, both list and search.
panel = panel.replace("    loadOrders(activeStatus);\n    loadInventory();\n", "    loadOrders(activeStatus);\n    loadFinancialSummary();\n    loadInventory();\n")

# Inventory names editable.
panel = rep(panel,
'''        <td>${p.name}${colorBadge}</td>''',
'''        <td><input type="text" class="product-name-input" data-name-input value="${escapeAttr(p.name)}" aria-label="Nombre del producto">${colorBadge}</td>''',
'inventory editable name')

panel = rep(panel,
'''      const priceInput = tr.querySelector('[data-price-input]');\n      saveBtn.disabled = true;''',
'''      const priceInput = tr.querySelector('[data-price-input]');\n      const nameInput = tr.querySelector('[data-name-input]');\n      const productName = nameInput ? nameInput.value.trim() : '';\n      if (!productName) { showMsg(msgEl, 'El nombre del producto no puede quedar vacío.', 'error'); return; }\n      saveBtn.disabled = true;''',
'inventory name read')

panel = rep(panel,
'''      if (!failed && priceInput) {\n        const price = parseFloat(priceInput.value);\n        if (!isNaN(price) && price > 0) {\n          const { error: priceErr } = await client.from('products').update({ regular_price: price }).eq('id', saveBtn.dataset.productId);\n          if (priceErr) failed = priceErr;\n        }\n      }''',
'''      if (!failed && priceInput) {\n        const price = parseFloat(priceInput.value);\n        if (!isNaN(price) && price > 0) {\n          const { error: productErr } = await client.from('products').update({ regular_price: price, name: productName }).eq('id', saveBtn.dataset.productId);\n          if (productErr) failed = productErr;\n        } else {\n          const { error: productErr } = await client.from('products').update({ name: productName }).eq('id', saveBtn.dataset.productId);\n          if (productErr) failed = productErr;\n        }\n      }''',
'inventory save name')
panel = panel.replace("      showMsg(msgEl, 'Inventario actualizado.', 'ok');", "      showMsg(msgEl, 'Producto actualizado. El nombre, precio y stock se reflejarán en el catálogo.', 'ok');", 1)

# Color saving via normalized RPC: exact existing color updates instead of duplicates.
panel = rep(panel,
'''  async function loadColorProductOptions(selectedId = null) {\n    const select = document.getElementById('colorProductSelect');\n    const { data, error } = await client.from('products').select('id, name, uses_color_variants').order('name');''',
'''  async function loadColorProductOptions(selectedId = null) {\n    const select = document.getElementById('colorProductSelect');\n    const { data, error } = await client.from('products').select('id, name, uses_color_variants, color_stock_mode').order('name');''',
'color product options meta')

old_color_save = '''    const stocks = {};\n    SIZE_ORDER.forEach(s => { stocks[s] = Math.max(0, parseInt(document.getElementById('variantColor' + s).value, 10) || 0); });\n    const rows = SIZE_ORDER.map(size => ({ product_id: productId, color, size, stock_on_hand: stocks[size] }));\n    const btn = document.getElementById('saveColorVariantBtn');\n    btn.disabled = true;\n    const { error } = await client.from('product_color_variants').upsert(rows, { onConflict: 'product_id,color,size' });\n    if (!error) {\n      const { error: flagErr } = await client.from('products').update({ uses_color_variants: true }).eq('id', productId);\n      if (flagErr) {\n        btn.disabled = false;\n        showMsg(msgEl, 'Los colores se guardaron, pero no se pudieron activar: ' + flagErr.message, 'error');\n        return;\n      }\n    }\n    btn.disabled = false;\n    if (error) { showMsg(msgEl, 'Error guardando color: ' + error.message, 'error'); return; }\n    showMsg(msgEl, `Color "${color}" guardado. El producto ya usa inventario por color y talla.`, 'ok');\n    await loadColorProductOptions(productId);\n    await loadInventory();'''
new_color_save = '''    const stocks = {};\n    SIZE_ORDER.forEach(s => { stocks[s] = Math.max(0, parseInt(document.getElementById('variantColor' + s).value, 10) || 0); });\n    const btn = document.getElementById('saveColorVariantBtn');\n    btn.disabled = true;\n    const { data, error } = await client.rpc('save_product_color_variant', {\n      p_product_id: productId,\n      p_color: color,\n      p_stocks: stocks\n    });\n    btn.disabled = false;\n    if (error) { showMsg(msgEl, 'Error guardando color: ' + error.message, 'error'); return; }\n    const saved = Array.isArray(data) ? data[0] : data;\n    const canonical = saved?.color || color;\n    const shared = saved?.stock_mode === 'shared_size';\n    const message = saved?.existed\n      ? `"${canonical}" ya existía: se actualizó la misma variante, no se creó un color duplicado.${shared ? ' El stock sigue administrándose por talla desde Inventario.' : ''}`\n      : `Color "${canonical}" agregado.${shared ? ' Usa el stock compartido del producto.' : ''} Aparecerá como opción en el catálogo al recargar.`;\n    showMsg(msgEl, message, 'ok');\n    document.getElementById('variantColorName').value = '';\n    await loadColorProductOptions(productId);\n    await loadInventory();'''
panel = rep(panel, old_color_save, new_color_save, 'normalized color save')

# Upcoming names editable and stored as upcoming-safe public metadata.
panel = rep(panel, ".select('slug, regular_price, active, published_once, product_variants(size, stock_on_hand)')", ".select('slug, name, regular_price, active, published_once, product_variants(size, stock_on_hand)')", 'upcoming select name')
panel = rep(panel,
'''      tr.innerHTML = `\n        <td>${item.name}</td>''',
'''      const displayName = existing?.name || item.name;\n      tr.innerHTML = `\n        <td><input type="text" class="upcoming-name-input" data-upcoming-name value="${escapeAttr(displayName)}" aria-label="Nombre del próximo drop"></td>''',
'upcoming editable name')
panel = rep(panel,
'''        <td class="row" style="gap:6px; flex-wrap:nowrap;">\n          <button class="secondary save-draft-btn" data-slug="${item.slug}" data-name="${item.name}">Guardar</button>\n          <button class="publish-btn" data-slug="${item.slug}" data-name="${item.name}">Publicar</button>\n        </td>''',
'''        <td><div class="actions-cell">\n          <button class="secondary save-draft-btn" data-slug="${item.slug}">Guardar</button>\n          <button class="publish-btn" data-slug="${item.slug}">Publicar</button>\n        </div></td>''',
'upcoming actions cell')
panel = rep(panel,
'''    const slug = btn.dataset.slug;\n    const name = btn.dataset.name;\n    const priceInput = tr.querySelector('[data-price]');''',
'''    const slug = btn.dataset.slug;\n    const nameInput = tr.querySelector('[data-upcoming-name]');\n    const name = nameInput ? nameInput.value.trim() : '';\n    if (!name) { showMsg(msgEl, 'El nombre del producto no puede quedar vacío.', 'error'); return; }\n    const priceInput = tr.querySelector('[data-price]');''',
'upcoming read editable name')
panel = rep(panel,
'''      slug, name, category: 'Jersey', sale_mode: 'in_stock',\n      regular_price: isNaN(price) ? 0 : price,\n      active: false,\n      published_once: false''',
'''      slug, name, category: 'Jersey', sale_mode: 'in_stock',\n      regular_price: isNaN(price) ? 0 : price,\n      active: false,\n      published_once: false,\n      is_upcoming: true''',
'upcoming draft flag')

# CSV message: remove unexplained record count.
panel = rep(panel, "    showMsg(exportMsg, `Descargado: ${data.length} solicitud(es).`, 'ok');", "    showMsg(exportMsg, 'CSV descargado correctamente.', 'ok');", 'csv success')

# ------------------------------------------------------------------
# INDEX — public names follow Supabase and new colors get real swatches
# ------------------------------------------------------------------
index = rep(index,
'''      renderAllSizeRows();\n      renderAllStatusTags();\n      renderAllPrices();''',
'''      renderAllSizeRows();\n      renderAllStatusTags();\n      renderAllProductNames();\n      renderAllPrices();''',
'index call product names')

status_to_prices = '''    function renderAllPrices() {\n'''
name_renderer = '''    function renderAllProductNames() {\n      document.querySelectorAll('[data-price-for]').forEach(priceEl => {\n        const slug = priceEl.dataset.priceFor;\n        const product = catalog[slug];\n        if (!product || !product.name) return;\n        const card = priceEl.closest('.card');\n        const title = card?.querySelector('h3');\n        if (title) title.textContent = product.name;\n        const purchaseBtn = card?.querySelector('[data-open-purchase]');\n        if (purchaseBtn) purchaseBtn.setAttribute('aria-label', `Comprar ${product.name} por Instagram`);\n      });\n    }\n\n'''
index = rep(index, status_to_prices, name_renderer + status_to_prices, 'index product name renderer')

old_sync_call = "      const { data, error } = await client.rpc('get_published_product_states');"
index = rep(index, old_sync_call, "      const { data, error } = await client.rpc('get_upcoming_catalog_states');", 'upcoming public state rpc')
index = rep(index,
'''        const state = states.get(tag.dataset.stockStatus);\n        if (!state || state.published_once !== true) return;\n\n        // Si ya se publicó alguna vez pero hoy está oculto, no debe volver a\n        // aparecer en Próximos Drops. Si está activo, migrateUpcomingCards()\n        // lo moverá inmediatamente al catálogo principal.\n        if (state.active !== true) card.remove();''',
'''        const state = states.get(tag.dataset.stockStatus);\n        if (!state) return;\n\n        if (state.name) {\n          const title = card.querySelector('h3');\n          if (title) title.textContent = state.name;\n          const purchaseBtn = card.querySelector('[data-open-purchase]');\n          if (purchaseBtn) purchaseBtn.setAttribute('aria-label', `Comprar ${state.name} por Instagram`);\n        }\n\n        if (state.published_once !== true) return;\n\n        // Si ya se publicó alguna vez pero hoy está oculto, no debe volver a\n        // aparecer en Próximos Drops. Si está activo, migrateUpcomingCards()\n        // lo moverá inmediatamente al catálogo principal.\n        if (state.active !== true) card.remove();''',
'upcoming public name sync')

old_swatches = '''      const COLOR_SWATCHES = {\n        'Burgundy': '#7B1E3A',\n        'Berenjena': '#4B2647',\n        'Azul marino': '#172A46'\n      };\n      colorsEl.innerHTML = hasColors ? product.colors.map(color => {\n        const swatch = COLOR_SWATCHES[color] || '#6B7280';'''
new_swatches = '''      const COLOR_SWATCHES = {\n        'burgundy': '#7B1E3A', 'berenjena': '#4B2647', 'azul marino': '#172A46',\n        'rojo': '#C62828', 'red': '#C62828', 'negro': '#202020', 'black': '#202020',\n        'blanco': '#F7F7F5', 'white': '#F7F7F5', 'crema': '#E8DDC5', 'beige': '#D8C7A6',\n        'azul': '#2F5DA8', 'celeste': '#77BDE8', 'verde': '#3E7B55', 'green': '#3E7B55',\n        'amarillo': '#E4B93F', 'naranja': '#D9772B', 'rosa': '#D978A0', 'rosado': '#D978A0',\n        'morado': '#6D4A8E', 'violeta': '#6D4A8E', 'gris': '#8A8F98', 'gray': '#8A8F98',\n        'marron': '#795548', 'cafe': '#795548'\n      };\n      colorsEl.innerHTML = hasColors ? product.colors.map(color => {\n        const key = String(color || '').trim().toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');\n        const swatch = COLOR_SWATCHES[key] || '#6B7280';'''
index = rep(index, old_swatches, new_swatches, 'index color swatches')

panel_path.write_text(panel, encoding='utf-8')
index_path.write_text(index, encoding='utf-8')
print('patched panel-privado.html and index.html')
