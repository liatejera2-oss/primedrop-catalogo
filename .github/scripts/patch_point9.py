from pathlib import Path

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
orig_index = index

# --- Public catalog CSS / modal color UI ---
old_css = """  .purchase-field label { display: block; font-size: 12.5px; font-weight: 600; color: var(--ink); margin-bottom: 8px; }
  .purchase-sizes { display: flex; gap: 8px; flex-wrap: wrap; }
"""
new_css = """  .purchase-field label { display: block; font-size: 12.5px; font-weight: 600; color: var(--ink); margin-bottom: 8px; }
  .purchase-colors, .purchase-sizes { display: flex; gap: 8px; flex-wrap: wrap; }
  .purchase-color-btn { font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; min-height: 40px; padding: 0 14px; border-radius: 6px; border: 1px solid var(--line); background: #fff; color: var(--ink); cursor: pointer; transition: border-color .15s ease, background .15s ease; }
  .purchase-color-btn[aria-pressed=\"true\"] { background: var(--ink); border-color: var(--ink); color: #fff; }
"""
if old_css not in index: raise SystemExit('purchase CSS anchor missing')
index = index.replace(old_css, new_css, 1)

old_modal = """      <div class=\"purchase-field\">
        <label>Talla</label>
        <div class=\"purchase-sizes\" id=\"purchaseSizes\" role=\"group\" aria-label=\"Selecciona una talla\"></div>
      </div>
"""
new_modal = """      <div class=\"purchase-field\" id=\"purchaseColorField\" hidden>
        <label>Color</label>
        <div class=\"purchase-colors\" id=\"purchaseColors\" role=\"group\" aria-label=\"Selecciona un color\"></div>
      </div>

      <div class=\"purchase-field\">
        <label>Talla</label>
        <div class=\"purchase-sizes\" id=\"purchaseSizes\" role=\"group\" aria-label=\"Selecciona una talla\"></div>
      </div>
"""
if old_modal not in index: raise SystemExit('purchase modal anchor missing')
index = index.replace(old_modal, new_modal, 1)

old_query = ".select('id, slug, name, regular_price, preorder_price, sale_mode, active, product_variants(id, size, stock_on_hand)')"
new_query = ".select('id, slug, name, regular_price, preorder_price, sale_mode, active, uses_color_variants, product_variants(id, size, stock_on_hand), product_color_variants(id, color, size, stock_on_hand)')"
if old_query not in index: raise SystemExit('catalog query anchor missing')
index = index.replace(old_query, new_query, 1)

old_build = """      data.forEach(p => {
        const variants = {};
        (p.product_variants || []).forEach(v => { variants[v.size] = v; });
        catalog[p.slug] = { ...p, variants };
      });
"""
new_build = """      data.forEach(p => {
        const variants = {};
        (p.product_variants || []).forEach(v => { variants[v.size] = v; });
        const colorVariants = {};
        (p.product_color_variants || []).forEach(v => {
          if (!colorVariants[v.color]) colorVariants[v.color] = {};
          colorVariants[v.color][v.size] = v;
        });
        const colors = Object.keys(colorVariants);
        catalog[p.slug] = { ...p, variants, colorVariants, colors };
      });
"""
if old_build not in index: raise SystemExit('catalog build anchor missing')
index = index.replace(old_build, new_build, 1)

old_total = """    function totalStock(product) {
      return SIZE_ORDER.reduce((sum, s) => sum + (product.variants[s] ? product.variants[s].stock_on_hand : 0), 0);
    }
"""
new_total = """    function totalStock(product) {
      if (product.uses_color_variants && product.colors && product.colors.length) {
        return product.colors.reduce((sum, color) => sum + SIZE_ORDER.reduce((inner, size) => {
          const variant = product.colorVariants[color]?.[size];
          return inner + (variant ? variant.stock_on_hand : 0);
        }, 0), 0);
      }
      return SIZE_ORDER.reduce((sum, s) => sum + (product.variants[s] ? product.variants[s].stock_on_hand : 0), 0);
    }

    function availableSizesForProduct(product, color = null) {
      if (product.uses_color_variants && product.colors && product.colors.length) {
        const source = color ? (product.colorVariants[color] || {}) : null;
        if (source) return SIZE_ORDER.filter(size => source[size]);
        return SIZE_ORDER.filter(size => product.colors.some(c => product.colorVariants[c]?.[size]));
      }
      return SIZE_ORDER.filter(size => product.variants[size]);
    }

    function stockForSelection(product, size, color = null) {
      if (product.uses_color_variants && product.colors && product.colors.length) {
        if (color) return product.colorVariants[color]?.[size]?.stock_on_hand ?? 0;
        return product.colors.reduce((sum, c) => sum + (product.colorVariants[c]?.[size]?.stock_on_hand ?? 0), 0);
      }
      return product.variants[size]?.stock_on_hand ?? 0;
    }
"""
if old_total not in index: raise SystemExit('totalStock anchor missing')
index = index.replace(old_total, new_total, 1)

old_render_sizes = """        let anyBackorder = false;
        row.innerHTML = SIZE_ORDER.filter(size => product.variants[size]).map(size => {
          const stock = product.variants[size].stock_on_hand;
          const backorder = product.sale_mode === 'in_stock' && stock <= 0;
          if (backorder) anyBackorder = true;
          return `<button type=\"button\" class=\"size-chip${backorder ? ' backorder' : ''}\" data-size=\"${size}\" data-stock=\"${stock}\">${size}</button>`;
        }).join('');
"""
new_render_sizes = """        let anyBackorder = false;
        const sizes = availableSizesForProduct(product);
        row.innerHTML = sizes.map(size => {
          const stock = stockForSelection(product, size);
          const backorder = product.sale_mode === 'in_stock' && stock <= 0;
          if (backorder) anyBackorder = true;
          return `<button type=\"button\" class=\"size-chip${backorder ? ' backorder' : ''}\" data-size=\"${size}\" data-stock=\"${stock}\">${size}</button>`;
        }).join('');
"""
if old_render_sizes not in index: raise SystemExit('render sizes anchor missing')
index = index.replace(old_render_sizes, new_render_sizes, 1)

old_caption = "caption.textContent = anyBackorder ? 'Talla punteada: disponible por pedido.' : '';"
new_caption = "caption.textContent = product.uses_color_variants ? 'Disponibilidad según color y talla.' : (anyBackorder ? 'Talla punteada: disponible por pedido.' : '');"
if old_caption not in index: raise SystemExit('caption anchor missing')
index = index.replace(old_caption, new_caption, 1)
old_display = "caption.style.display = anyBackorder ? '' : 'none';"
new_display = "caption.style.display = (product.uses_color_variants || anyBackorder) ? '' : 'none';"
index = index.replace(old_display, new_display, 1)

old_consts = """    const priceEl = document.getElementById('purchasePrice');
    const sizesEl = document.getElementById('purchaseSizes');
"""
new_consts = """    const priceEl = document.getElementById('purchasePrice');
    const colorFieldEl = document.getElementById('purchaseColorField');
    const colorsEl = document.getElementById('purchaseColors');
    const sizesEl = document.getElementById('purchaseSizes');
"""
if old_consts not in index: raise SystemExit('purchase const anchor missing')
index = index.replace(old_consts, new_consts, 1)

old_state = """    let currentSlug = null;
    let currentSize = null;
    let currentPaymentMode = 'full';
"""
new_state = """    let currentSlug = null;
    let currentColor = null;
    let currentSize = null;
    let currentPaymentMode = 'full';
"""
if old_state not in index: raise SystemExit('purchase state anchor missing')
index = index.replace(old_state, new_state, 1)

old_select_size = """    function selectSize(size) {
      currentSize = size;
      sizesEl.querySelectorAll('.purchase-size-btn').forEach(btn => {
        btn.setAttribute('aria-pressed', btn.dataset.size === size ? 'true' : 'false');
      });
      const product = catalog[currentSlug];
      const variant = product.variants[size];
      const stock = variant ? variant.stock_on_hand : 0;

      if (product.sale_mode === 'in_stock' && stock > 0) {
"""
new_select_size = """    function renderPurchaseSizes() {
      const product = catalog[currentSlug];
      if (!product) return [];
      const sizes = availableSizesForProduct(product, currentColor);
      sizesEl.innerHTML = sizes.map(size => {
        const stock = stockForSelection(product, size, currentColor);
        const backorder = product.sale_mode === 'in_stock' && stock <= 0;
        return `<button type=\"button\" class=\"purchase-size-btn${backorder ? ' backorder' : ''}\" data-size=\"${size}\" aria-pressed=\"false\">${size}</button>`;
      }).join('');
      return sizes;
    }

    function selectColor(color) {
      currentColor = color;
      currentSize = null;
      colorsEl.querySelectorAll('.purchase-color-btn').forEach(btn => {
        btn.setAttribute('aria-pressed', btn.dataset.color === color ? 'true' : 'false');
      });
      const sizes = renderPurchaseSizes();
      if (sizes.length) selectSize(sizes[0]);
      else {
        qtyInput.value = 1;
        qtyInput.max = 1;
        stockNoteEl.textContent = 'No hay tallas configuradas para este color.';
      }
    }

    function selectSize(size) {
      currentSize = size;
      sizesEl.querySelectorAll('.purchase-size-btn').forEach(btn => {
        btn.setAttribute('aria-pressed', btn.dataset.size === size ? 'true' : 'false');
      });
      const product = catalog[currentSlug];
      const stock = stockForSelection(product, size, currentColor);

      if (product.sale_mode === 'in_stock' && stock > 0) {
"""
if old_select_size not in index: raise SystemExit('selectSize anchor missing')
index = index.replace(old_select_size, new_select_size, 1)

old_open = """      currentSlug = slug;
      currentSize = null;
      errorEl.hidden = true;
"""
new_open = """      currentSlug = slug;
      currentColor = null;
      currentSize = null;
      errorEl.hidden = true;
"""
index = index.replace(old_open, new_open, 1)

old_available = """      const availableSizes = SIZE_ORDER.filter(s => product.variants[s]);
      sizesEl.innerHTML = availableSizes.map(size => {
        const stock = product.variants[size].stock_on_hand;
        const backorder = product.sale_mode === 'in_stock' && stock <= 0;
        return `<button type=\"button\" class=\"purchase-size-btn${backorder ? ' backorder' : ''}\" data-size=\"${size}\" aria-pressed=\"false\">${size}</button>`;
      }).join('');

      selectPaymentMode('full');

      if (availableSizes.length) {
        selectSize(availableSizes[0]);
      } else {
"""
new_available = """      const hasColors = product.uses_color_variants && product.colors && product.colors.length;
      colorFieldEl.hidden = !hasColors;
      colorsEl.innerHTML = hasColors ? product.colors.map(color =>
        `<button type=\"button\" class=\"purchase-color-btn\" data-color=\"${color}\" aria-pressed=\"false\">${color}</button>`
      ).join('') : '';

      selectPaymentMode('full');
      let availableSizes = [];
      if (hasColors) {
        selectColor(product.colors[0]);
        availableSizes = availableSizesForProduct(product, product.colors[0]);
      } else {
        availableSizes = renderPurchaseSizes();
        if (availableSizes.length) selectSize(availableSizes[0]);
      }

      if (!availableSizes.length) {
"""
if old_available not in index: raise SystemExit('openModal availableSizes anchor missing')
index = index.replace(old_available, new_available, 1)

old_size_listener = """    sizesEl.addEventListener('click', (e) => {
      const btn = e.target.closest('.purchase-size-btn');
      if (!btn || btn.disabled) return;
      selectSize(btn.dataset.size);
    });
"""
new_size_listener = """    colorsEl.addEventListener('click', (e) => {
      const btn = e.target.closest('.purchase-color-btn');
      if (!btn) return;
      selectColor(btn.dataset.color);
    });

    sizesEl.addEventListener('click', (e) => {
      const btn = e.target.closest('.purchase-size-btn');
      if (!btn || btn.disabled) return;
      selectSize(btn.dataset.size);
    });
"""
if old_size_listener not in index: raise SystemExit('size listener anchor missing')
index = index.replace(old_size_listener, new_size_listener, 1)

old_submit = """      const { data, error } = await client.rpc('create_purchase_request', {
        p_product_slug: currentSlug,
        p_size: currentSize,
        p_quantity: qty,
        p_payment_mode: currentPaymentMode
      });
"""
new_submit = """      const product = catalog[currentSlug];
      if (product.uses_color_variants && !currentColor) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Continuar';
        errorEl.textContent = 'Selecciona un color.';
        errorEl.hidden = false;
        return;
      }
      const rpcName = product.uses_color_variants ? 'create_purchase_request_variant' : 'create_purchase_request';
      const rpcArgs = product.uses_color_variants ? {
        p_product_slug: currentSlug,
        p_color: currentColor,
        p_size: currentSize,
        p_quantity: qty,
        p_payment_mode: currentPaymentMode
      } : {
        p_product_slug: currentSlug,
        p_size: currentSize,
        p_quantity: qty,
        p_payment_mode: currentPaymentMode
      };
      const { data, error } = await client.rpc(rpcName, rpcArgs);
"""
if old_submit not in index: raise SystemExit('purchase RPC anchor missing')
index = index.replace(old_submit, new_submit, 1)

old_msg = """        `Producto: ${row.product_name}\n` +
        `Talla: ${row.size}\n` +
"""
new_msg = """        `Producto: ${row.product_name}\n` +
        (row.color ? `Color: ${row.color}\n` : '') +
        `Talla: ${row.size}\n` +
"""
if old_msg not in index: raise SystemExit('message anchor missing')
index = index.replace(old_msg, new_msg, 1)

# --- Private panel: color manager and inventory aggregation ---
panel_path = Path('panel-privado.html')
panel = panel_path.read_text(encoding='utf-8')
orig_panel = panel

old_inv_close = """      </div>
    </div>

    <div id=\"viewProximos\" class=\"view-section hidden\">
"""
new_inv_close = """      </div>

      <div class=\"card\" id=\"colorVariantsCard\">
        <h2>Variantes de color</h2>
        <p class=\"sub\" style=\"margin-bottom:14px;\">Usa esta sección solo cuando una misma pieza se vende en varios colores. El stock se controla por combinación de color y talla. Los productos que no usan color continúan funcionando como hasta ahora.</p>
        <div id=\"colorVariantsMsg\"></div>
        <div class=\"row\" style=\"align-items:flex-end; margin-bottom:14px;\">
          <div style=\"flex:2; min-width:220px;\">
            <label for=\"colorProductSelect\">Producto</label>
            <select id=\"colorProductSelect\" style=\"width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:var(--radius-sm); font-family:inherit; font-size:14px;\"></select>
          </div>
          <div style=\"flex:1; min-width:150px;\">
            <label for=\"variantColorName\">Color</label>
            <input type=\"text\" id=\"variantColorName\" placeholder=\"Ej. Negro\" style=\"margin-bottom:0;\">
          </div>
          <div><label>S</label><input type=\"number\" min=\"0\" id=\"variantColorS\" value=\"0\" style=\"width:64px; margin-bottom:0;\"></div>
          <div><label>M</label><input type=\"number\" min=\"0\" id=\"variantColorM\" value=\"0\" style=\"width:64px; margin-bottom:0;\"></div>
          <div><label>L</label><input type=\"number\" min=\"0\" id=\"variantColorL\" value=\"0\" style=\"width:64px; margin-bottom:0;\"></div>
          <div><label>XL</label><input type=\"number\" min=\"0\" id=\"variantColorXL\" value=\"0\" style=\"width:64px; margin-bottom:0;\"></div>
          <button id=\"saveColorVariantBtn\">Guardar color</button>
        </div>
        <div class=\"row\" style=\"margin-bottom:14px;\">
          <button class=\"secondary\" id=\"disableColorVariantsBtn\">Desactivar colores para este producto</button>
          <span class=\"sub\" style=\"margin:0;\">Desactivar no borra los datos; solo vuelve temporalmente al stock tradicional por talla.</span>
        </div>
        <div class=\"table-scroll\">
          <table>
            <thead><tr><th>Color</th><th>S</th><th>M</th><th>L</th><th>XL</th><th>Total</th></tr></thead>
            <tbody id=\"colorVariantsBody\"></tbody>
          </table>
        </div>
      </div>
    </div>

    <div id=\"viewProximos\" class=\"view-section hidden\">
"""
if old_inv_close not in panel: raise SystemExit('inventory close anchor missing')
panel = panel.replace(old_inv_close, new_inv_close, 1)

old_panel_query = ".select('id, slug, name, sale_mode, regular_price, active, published_once, product_variants(id, size, stock_on_hand)')"
new_panel_query = ".select('id, slug, name, sale_mode, regular_price, active, published_once, uses_color_variants, product_variants(id, size, stock_on_hand), product_color_variants(id, color, size, stock_on_hand)')"
if old_panel_query not in panel: raise SystemExit('panel inventory query anchor missing')
panel = panel.replace(old_panel_query, new_panel_query, 1)

old_rows_start = """    rows.forEach(p => {
      const variants = {};
      (p.product_variants || []).forEach(v => { variants[v.size] = v; });
      const total = SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);

      const tr = document.createElement('tr');
      const sizeCells = SIZE_ORDER.map(s => {
        const v = variants[s];
        if (!v) return '<td>—</td>';
        return `<td><input type=\"number\" min=\"0\" class=\"stock-input\" data-variant-id=\"${v.id}\" value=\"${v.stock_on_hand}\"></td>`;
      }).join('');
"""
new_rows_start = """    rows.forEach(p => {
      const variants = {};
      (p.product_variants || []).forEach(v => { variants[v.size] = v; });
      const colorVariants = p.product_color_variants || [];
      const colorTotalBySize = {};
      SIZE_ORDER.forEach(size => { colorTotalBySize[size] = colorVariants.filter(v => v.size === size).reduce((sum, v) => sum + v.stock_on_hand, 0); });
      const total = p.uses_color_variants
        ? SIZE_ORDER.reduce((sum, s) => sum + colorTotalBySize[s], 0)
        : SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);

      const tr = document.createElement('tr');
      const sizeCells = SIZE_ORDER.map(s => {
        if (p.uses_color_variants) return `<td>${colorTotalBySize[s]}</td>`;
        const v = variants[s];
        if (!v) return '<td>—</td>';
        return `<td><input type=\"number\" min=\"0\" class=\"stock-input\" data-variant-id=\"${v.id}\" value=\"${v.stock_on_hand}\"></td>`;
      }).join('');
"""
if old_rows_start not in panel: raise SystemExit('inventory row anchor missing')
panel = panel.replace(old_rows_start, new_rows_start, 1)

old_name_td = "<td>${p.name}</td>"
new_name_td = "<td>${p.name}${p.uses_color_variants ? ' <span class=\"badge badge-full\">Colores</span>' : ''}</td>"
panel = panel.replace(old_name_td, new_name_td, 1)

old_buttons = """          <button class=\"secondary save-stock-btn\" data-product-id=\"${p.id}\">Guardar</button>
          <button class=\"${p.active ? 'danger' : 'secondary'} toggle-active-btn\" data-product-id=\"${p.id}\" data-active=\"${p.active ? '1' : '0'}\" data-name=\"${p.name}\" title=\"${p.active ? 'Bajar del catálogo público' : 'Publicar en el catálogo público'}\">${p.active ? 'Bajar' : 'Publicar'}</button>
"""
new_buttons = """          <button class=\"secondary save-stock-btn\" data-product-id=\"${p.id}\">${p.uses_color_variants ? 'Guardar precio' : 'Guardar'}</button>
          <button class=\"secondary edit-colors-btn\" data-product-id=\"${p.id}\">Colores</button>
          <button class=\"${p.active ? 'danger' : 'secondary'} toggle-active-btn\" data-product-id=\"${p.id}\" data-active=\"${p.active ? '1' : '0'}\" data-name=\"${p.name}\" title=\"${p.active ? 'Bajar del catálogo público' : 'Publicar en el catálogo público'}\">${p.active ? 'Bajar' : 'Publicar'}</button>
"""
if old_buttons not in panel: raise SystemExit('inventory buttons anchor missing')
panel = panel.replace(old_buttons, new_buttons, 1)

old_click_vars = """    const saveBtn = e.target.closest('.save-stock-btn');
    const toggleBtn = e.target.closest('.toggle-active-btn');
"""
new_click_vars = """    const saveBtn = e.target.closest('.save-stock-btn');
    const editColorsBtn = e.target.closest('.edit-colors-btn');
    const toggleBtn = e.target.closest('.toggle-active-btn');
"""
panel = panel.replace(old_click_vars, new_click_vars, 1)

anchor_before_toggle = """    if (toggleBtn) {
"""
color_click = """    if (editColorsBtn) {
      const select = document.getElementById('colorProductSelect');
      select.value = editColorsBtn.dataset.productId;
      await loadColorVariants();
      document.getElementById('colorVariantsCard').scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }

"""
if anchor_before_toggle not in panel: raise SystemExit('toggle anchor missing')
panel = panel.replace(anchor_before_toggle, color_click + anchor_before_toggle, 1)

# Add color manager functions before Próximos drops section.
manager_anchor = """  // ---- Próximos drops: preparar precio/tallas y publicar al catálogo ----
"""
manager_code = """  // ---- Variantes de color ----
  async function loadColorProductOptions(selectedId = null) {
    const select = document.getElementById('colorProductSelect');
    const { data, error } = await client.from('products').select('id, name, uses_color_variants').order('name');
    if (error) return;
    const current = selectedId || select.value;
    select.innerHTML = (data || []).map(p => `<option value=\"${p.id}\">${p.name}${p.uses_color_variants ? ' · colores activos' : ''}</option>`).join('');
    if (current && (data || []).some(p => p.id === current)) select.value = current;
    await loadColorVariants();
  }

  async function loadColorVariants() {
    const productId = document.getElementById('colorProductSelect').value;
    const tbody = document.getElementById('colorVariantsBody');
    const msgEl = document.getElementById('colorVariantsMsg');
    tbody.innerHTML = '';
    showMsg(msgEl, '', null);
    if (!productId) return;
    const { data, error } = await client.from('product_color_variants')
      .select('id, color, size, stock_on_hand')
      .eq('product_id', productId)
      .order('color');
    if (error) { showMsg(msgEl, 'Error cargando colores: ' + error.message, 'error'); return; }
    const grouped = {};
    (data || []).forEach(v => {
      if (!grouped[v.color]) grouped[v.color] = {};
      grouped[v.color][v.size] = v;
    });
    const colors = Object.keys(grouped);
    if (!colors.length) {
      tbody.innerHTML = '<tr><td colspan=\"6\" style=\"color:var(--ink-soft);\">Este producto todavía no tiene colores configurados.</td></tr>';
      return;
    }
    colors.forEach(color => {
      const total = SIZE_ORDER.reduce((sum, s) => sum + (grouped[color][s]?.stock_on_hand || 0), 0);
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${color}</td>${SIZE_ORDER.map(s => `<td>${grouped[color][s]?.stock_on_hand ?? 0}</td>`).join('')}<td>${total}</td>`;
      tbody.appendChild(tr);
    });
  }

  document.getElementById('colorProductSelect').addEventListener('change', loadColorVariants);

  document.getElementById('saveColorVariantBtn').addEventListener('click', async () => {
    const msgEl = document.getElementById('colorVariantsMsg');
    const productId = document.getElementById('colorProductSelect').value;
    const color = document.getElementById('variantColorName').value.trim();
    if (!productId || !color) { showMsg(msgEl, 'Selecciona un producto y escribe el color.', 'error'); return; }
    const stocks = {};
    SIZE_ORDER.forEach(s => { stocks[s] = Math.max(0, parseInt(document.getElementById('variantColor' + s).value, 10) || 0); });
    const rows = SIZE_ORDER.map(size => ({ product_id: productId, color, size, stock_on_hand: stocks[size] }));
    const btn = document.getElementById('saveColorVariantBtn');
    btn.disabled = true;
    const { error } = await client.from('product_color_variants').upsert(rows, { onConflict: 'product_id,color,size' });
    if (!error) {
      const { error: flagErr } = await client.from('products').update({ uses_color_variants: true }).eq('id', productId);
      if (flagErr) {
        btn.disabled = false;
        showMsg(msgEl, 'Los colores se guardaron, pero no se pudieron activar: ' + flagErr.message, 'error');
        return;
      }
    }
    btn.disabled = false;
    if (error) { showMsg(msgEl, 'Error guardando color: ' + error.message, 'error'); return; }
    showMsg(msgEl, `Color \"${color}\" guardado. El producto ya usa inventario por color y talla.`, 'ok');
    await loadColorProductOptions(productId);
    await loadInventory();
  });

  document.getElementById('disableColorVariantsBtn').addEventListener('click', async () => {
    const productId = document.getElementById('colorProductSelect').value;
    const msgEl = document.getElementById('colorVariantsMsg');
    if (!productId) return;
    if (!confirm('¿Desactivar las variantes de color para este producto? Los datos de color se conservarán.')) return;
    const { error } = await client.from('products').update({ uses_color_variants: false }).eq('id', productId);
    if (error) { showMsg(msgEl, 'Error desactivando colores: ' + error.message, 'error'); return; }
    showMsg(msgEl, 'Variantes de color desactivadas. El producto vuelve a usar stock por talla.', 'ok');
    await loadColorProductOptions(productId);
    await loadInventory();
  });

"""
if manager_anchor not in panel: raise SystemExit('manager insertion anchor missing')
panel = panel.replace(manager_anchor, manager_code + manager_anchor, 1)

# Load options whenever inventory loads.
old_load_end = """      tbody.appendChild(tr);
    });
  }

  document.getElementById('inventoryBody').addEventListener('click', async (e) => {
"""
new_load_end = """      tbody.appendChild(tr);
    });
    await loadColorProductOptions();
  }

  document.getElementById('inventoryBody').addEventListener('click', async (e) => {
"""
if old_load_end not in panel: raise SystemExit('inventory end anchor missing')
panel = panel.replace(old_load_end, new_load_end, 1)

# Order search: include/display color if present.
old_order_select = ".select('quantity, unit_price, product_variants(size, products(name))')"
new_order_select = ".select('quantity, unit_price, product_variants(size, products(name)), product_color_variants(color, size)')"
if old_order_select not in panel: raise SystemExit('order item query anchor missing')
panel = panel.replace(old_order_select, new_order_select, 1)

old_item_html = """    const itemsHtml = (items || []).map(it =>
      `${it.product_variants.products.name} — talla ${it.product_variants.size} × ${it.quantity} (${moneyFmt(it.unit_price)} c/u)`
    ).join('<br>');
"""
new_item_html = """    const itemsHtml = (items || []).map(it => {
      const color = it.product_color_variants?.color;
      return `${it.product_variants.products.name}${color ? ` — color ${color}` : ''} — talla ${it.product_variants.size} × ${it.quantity} (${moneyFmt(it.unit_price)} c/u)`;
    }).join('<br>');
"""
if old_item_html not in panel: raise SystemExit('order item html anchor missing')
panel = panel.replace(old_item_html, new_item_html, 1)

if index == orig_index or panel == orig_panel:
    raise SystemExit('Point 9 patch did not modify both files')

for needle in [
  'purchaseColorField', 'create_purchase_request_variant', 'product_color_variants',
  'uses_color_variants', 'Variantes de color', 'saveColorVariantBtn', 'Color: ${row.color}'
]:
    if needle not in index + panel: raise SystemExit('missing expected: ' + needle)

index_path.write_text(index, encoding='utf-8')
panel_path.write_text(panel, encoding='utf-8')
