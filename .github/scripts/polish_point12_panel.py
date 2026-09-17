from pathlib import Path
import re

path = Path('panel-privado.html')
s = path.read_text(encoding='utf-8')
original = s


def replace_once(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'{label} anchor not found')
    s = s.replace(old, new, 1)

# ---------------------------------------------------------------------------
# 1) Visual system: wider workspace, clearer hierarchy, calmer controls,
#    friendlier responsive tables and collapsible secondary tools.
# ---------------------------------------------------------------------------
visual_css = r'''
<style id="point12-panel-polish">
  :root {
    --panel-bg: #F7F7F5;
    --panel-card: #FFFFFF;
    --panel-muted: #F3F3F1;
    --panel-line: #E4E4E1;
    --panel-ink: #1F1F1F;
    --panel-soft: #747474;
    --panel-red-soft: #FFF1F1;
  }
  body { background: var(--panel-bg); padding: 28px 24px 48px; }
  .wrap { max-width: 1180px; }
  .admin-title { display:flex; align-items:flex-end; justify-content:space-between; gap:20px; margin-bottom:22px; }
  .admin-eyebrow { display:block; margin-bottom:6px; font-size:10.5px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); }
  .admin-title h1 { font-size:24px; letter-spacing:-.025em; margin:0 0 4px; }
  .admin-title .sub { margin:0; }
  .panel-toolbar { display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:18px; padding:0 2px; }
  .panel-toolbar .sub { margin:0; font-size:12.5px; }
  .panel-nav { display:flex; gap:6px; padding:5px; width:max-content; max-width:100%; overflow-x:auto; background:#ECECE9; border-radius:999px; margin-bottom:22px; }
  .panel-nav .view-tab-btn { border:0; background:transparent; padding:9px 18px; white-space:nowrap; }
  .panel-nav .view-tab-btn.active { background:#fff; color:var(--ink); box-shadow:0 1px 3px rgba(0,0,0,.08); }
  .card { border-color:var(--panel-line); border-radius:16px; padding:22px; box-shadow:0 1px 0 rgba(0,0,0,.015); }
  .compact-card { padding:18px 20px; }
  .card h2 { font-size:16px; letter-spacing:-.01em; margin-bottom:6px; }
  .section-intro { margin:0 0 16px; color:var(--ink-soft); font-size:13px; line-height:1.5; max-width:820px; }
  button { min-height:38px; padding:8px 15px; }
  button.secondary { background:#fff; }
  button.danger { background:var(--accent); }
  button.danger-ghost { background:#fff; color:var(--accent); border:1px solid #F2C9CC; }
  button.danger-ghost:hover { background:var(--panel-red-soft); }
  input[type="email"], input[type="password"], input[type="text"], input[type="number"], input[type="date"], select {
    border-color:var(--panel-line); background:#fff; min-height:40px;
  }
  input:focus, select:focus, button:focus-visible, summary:focus-visible { outline:2px solid rgba(194,16,27,.18); outline-offset:2px; }
  .search-card { display:grid; grid-template-columns:minmax(180px,1fr) auto; align-items:end; gap:12px; }
  .search-card h2 { grid-column:1/-1; }
  .search-card .row { display:contents; }
  .search-card input { max-width:none !important; }
  .policy-details, .export-details, .advanced-details { border:1px solid var(--panel-line); border-radius:12px; background:#FAFAF8; margin:10px 0 16px; }
  .policy-details summary, .export-details summary, .advanced-details summary { list-style:none; cursor:pointer; padding:12px 14px; font-size:12.5px; font-weight:700; }
  .policy-details summary::-webkit-details-marker, .export-details summary::-webkit-details-marker, .advanced-details summary::-webkit-details-marker { display:none; }
  .policy-details summary::after, .export-details summary::after, .advanced-details summary::after { content:'+'; float:right; color:var(--ink-soft); font-size:16px; line-height:1; }
  .policy-details[open] summary::after, .export-details[open] summary::after, .advanced-details[open] summary::after { content:'−'; }
  .details-body { padding:0 14px 14px; color:var(--ink-soft); font-size:12.5px; line-height:1.55; }
  .export-controls { display:flex; gap:10px; align-items:end; flex-wrap:wrap; }
  .export-controls label { margin-bottom:5px; }
  .export-controls input { margin:0; }
  .tabs { gap:6px; flex-wrap:wrap; }
  .tab-btn { padding:8px 14px; min-height:36px; background:#fff; }
  .tab-btn.active { background:var(--ink); }
  .table-scroll { border:1px solid var(--panel-line); border-radius:12px; background:#fff; }
  .table-scroll table { min-width:100%; }
  th, td { padding:11px 10px; vertical-align:middle; }
  th { background:#FAFAF8; font-size:10.5px; }
  tbody tr:last-child td { border-bottom:0; }
  tbody tr:hover { background:#FCFCFA; }
  .orders-scroll table { min-width:960px; }
  .inventory-scroll table { min-width:1030px; }
  .upcoming-scroll table { min-width:860px; }
  .actions-cell { display:flex; gap:6px; align-items:center; flex-wrap:wrap; }
  .actions-cell button { min-height:32px; padding:5px 10px; font-size:12px; }
  .badge { border-radius:999px; padding:4px 9px; }
  .stock-state { font-size:12px; font-weight:700; }
  .stock-ok { color:#33764A; }
  .stock-low { color:var(--accent); }
  .color-dot { width:14px; height:14px; display:inline-block; vertical-align:-2px; border-radius:50%; border:1px solid rgba(0,0,0,.12); margin-right:7px; }
  .color-mode-note { margin:10px 0 14px; padding:10px 12px; border-radius:10px; background:#F6F4FF; color:#5A3BA4; font-size:12.5px; }
  .collapsible-card { padding:0; overflow:hidden; }
  .collapsible-card > summary { list-style:none; cursor:pointer; padding:19px 22px; display:flex; align-items:center; justify-content:space-between; gap:18px; }
  .collapsible-card > summary::-webkit-details-marker { display:none; }
  .collapsible-card > summary::after { content:'+'; width:28px; height:28px; display:grid; place-items:center; flex:0 0 auto; border:1px solid var(--panel-line); border-radius:50%; color:var(--ink-soft); }
  .collapsible-card[open] > summary::after { content:'−'; }
  .collapsible-card > summary strong { display:block; font-size:15px; margin-bottom:3px; }
  .collapsible-card > summary span { display:block; color:var(--ink-soft); font-size:12.5px; font-weight:400; }
  .collapsible-content { padding:0 22px 22px; }
  .subsection-title { font-size:13px; font-weight:700; margin:20px 0 8px; }
  .helper-text { color:var(--ink-soft); font-size:12.5px; line-height:1.45; }
  .inventory-note { display:flex; align-items:flex-start; gap:8px; margin-bottom:16px; padding:10px 12px; border-radius:10px; background:#FAFAF8; color:var(--ink-soft); font-size:12.5px; line-height:1.45; }
  .inventory-note strong { color:var(--ink); }
  input.stock-input { border-radius:8px; }
  input.stock-input[data-price-input], input.stock-input[data-price] { width:72px; }
  .table-scroll button { padding:6px 11px; }
  @media (max-width: 760px) {
    body { padding:18px 14px 36px; }
    .admin-title { align-items:flex-start; }
    .panel-toolbar { align-items:flex-start; flex-direction:column; }
    .panel-toolbar .row { width:100%; }
    .panel-toolbar button { flex:1; }
    .panel-nav { width:100%; border-radius:14px; }
    .panel-nav .view-tab-btn { flex:1; }
    .card { padding:17px; border-radius:14px; }
    .search-card { grid-template-columns:1fr; }
    .search-card h2 { grid-column:auto; }
    .search-card .row { display:flex; }
    .search-card button { width:100%; }
    .export-controls > div { flex:1 1 130px; }
    .export-controls button { width:100%; }
    .collapsible-content { padding:0 17px 17px; }
    .collapsible-card > summary { padding:17px; }
  }
</style>
'''
replace_once('</head>', visual_css + '\n</head>', 'head')

# ---------------------------------------------------------------------------
# 2) Cleaner title / toolbar / navigation.
# ---------------------------------------------------------------------------
replace_once(
'''  <h1>Prime Drop — Panel privado</h1>\n  <p class="sub">Solicitudes, inventario y confirmación de pagos. Acceso restringido a administradores.</p>''',
'''  <div class="admin-title">\n    <div>\n      <span class="admin-eyebrow">PRIME DROP / OPERATIONS</span>\n      <h1>Panel privado</h1>\n      <p class="sub">Ventas, reservas e inventario en un solo lugar.</p>\n    </div>\n  </div>''',
'admin title')

replace_once(
'''    <div class="row" style="justify-content: space-between; margin-bottom: 20px;">\n      <p class="sub" id="sessionInfo" style="margin:0;"></p>\n      <div class="row" style="gap:8px;">\n        <button class="secondary" id="refreshBtn" title="Actualizar datos">↻ Actualizar</button>\n        <button class="secondary" id="logoutBtn">Cerrar sesión</button>\n      </div>\n    </div>\n\n    <div class="tabs" style="margin-bottom:24px;">''',
'''    <div class="panel-toolbar">\n      <p class="sub" id="sessionInfo"></p>\n      <div class="row" style="gap:8px;">\n        <button class="secondary" id="refreshBtn" title="Actualizar datos">↻ Actualizar</button>\n        <button class="secondary" id="logoutBtn">Cerrar sesión</button>\n      </div>\n    </div>\n\n    <div class="panel-nav">''',
'toolbar navigation')

# ---------------------------------------------------------------------------
# 3) Solicitudes: reduce visual noise; keep operational rules accessible.
# ---------------------------------------------------------------------------
replace_once('<div class="card">\n        <h2>Buscar solicitud por código</h2>', '<div class="card compact-card search-card">\n        <h2>Buscar solicitud</h2>', 'search card')

reservation_rule = '''        <p class="sub" style="margin-bottom:14px;"><strong>Regla interna de reserva:</strong> una solicitud con abono no aparta stock hasta que confirmes el 50%. Al confirmar el abono pasa a <strong>Reservadas</strong> y el inventario se descuenta una sola vez. Al cobrar el saldo pasa a Pagadas sin volver a descontar. Si cancelas una reserva, el stock se libera; cualquier devolución de dinero se gestiona manualmente. Las reservas con abono confirmado no vencen automáticamente.</p>'''
reservation_details = '''        <p class="section-intro">Gestiona cada solicitud según el pago recibido. Los cambios de estado actualizan la reserva y el inventario automáticamente.</p>\n        <details class="policy-details">\n          <summary>Cómo funciona una reserva con abono 50%</summary>\n          <div class="details-body">La solicitud no aparta stock mientras esté Pendiente. Al confirmar el abono pasa a Reservada y el stock se descuenta una sola vez. Al completar el saldo pasa a Pagada sin descontar nuevamente. Cancelar una reserva libera el stock; cualquier devolución de dinero se gestiona manualmente. Las reservas confirmadas no vencen automáticamente.</div>\n        </details>'''
replace_once(reservation_rule, reservation_details, 'reservation rule')

export_old = '''        <div class="row" style="margin-bottom:16px; align-items:flex-end;">\n          <div>\n            <label for="exportFrom">Desde</label>\n            <input type="date" id="exportFrom" style="margin-bottom:0;">\n          </div>\n          <div>\n            <label for="exportTo">Hasta</label>\n            <input type="date" id="exportTo" style="margin-bottom:0;">\n          </div>\n          <button class="secondary" id="exportCsvBtn">Descargar CSV</button>\n          <span class="sub" style="margin:0;">Vacío en ambas fechas = descarga todas las solicitudes.</span>\n        </div>'''
export_new = '''        <details class="export-details">\n          <summary>Exportar solicitudes</summary>\n          <div class="details-body">\n            <div class="export-controls">\n              <div><label for="exportFrom">Desde</label><input type="date" id="exportFrom"></div>\n              <div><label for="exportTo">Hasta</label><input type="date" id="exportTo"></div>\n              <button class="secondary" id="exportCsvBtn">Descargar CSV</button>\n              <span class="helper-text">Sin fechas descarga todo el historial.</span>\n            </div>\n          </div>\n        </details>'''
replace_once(export_old, export_new, 'export controls')

orders_table = '''        <table>\n          <thead>\n            <tr><th>Código</th><th>Total</th><th>Cobrado / saldo</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>\n          </thead>\n          <tbody id="ordersBody"></tbody>\n        </table>'''
orders_table_new = '''        <div class="table-scroll orders-scroll">\n          <table>\n            <thead>\n              <tr><th>Código</th><th>Total</th><th>Cobrado / saldo</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>\n            </thead>\n            <tbody id="ordersBody"></tbody>\n          </table>\n        </div>'''
replace_once(orders_table, orders_table_new, 'orders table')

# ---------------------------------------------------------------------------
# 4) Inventory: concise guidance, fix shared-color stock presentation, declutter.
# ---------------------------------------------------------------------------
replace_once(
'''        <p class="sub" style="margin-bottom:14px;">Los cambios se guardan al presionar "Guardar" en cada fila. Esto corrige existencias manualmente — no reemplaza el descuento automático al confirmar un pago. La columna "Catálogo" controla si la prenda se ve en la página pública, sin importar el stock que tenga.</p>''',
'''        <p class="section-intro">Actualiza precio, stock y visibilidad del catálogo. Las ventas y reservas confirmadas descuentan inventario automáticamente.</p>\n        <div class="inventory-note"><span>ⓘ</span><span><strong>Catálogo</strong> solo controla si la pieza se ve públicamente. Ocultarla no elimina su inventario.</span></div>''',
'inventory intro')
replace_once('<div class="table-scroll">\n        <table>\n          <thead>\n            <tr><th>Producto</th><th>Precio</th><th>S</th><th>M</th><th>L</th><th>XL</th><th>Total</th><th>Estado</th><th>Catálogo</th><th></th></tr>', '<div class="table-scroll inventory-scroll">\n        <table>\n          <thead>\n            <tr><th>Producto</th><th>Precio</th><th>S</th><th>M</th><th>L</th><th>XL</th><th>Total</th><th>Estado</th><th>Catálogo</th><th>Acciones</th></tr>', 'inventory table')

# Turn the color manager into a secondary, collapsible tool.
color_block_pattern = re.compile(r'''      <div class="card" id="colorVariantsCard">.*?      </div>\n    </div>\n\n    <div id="viewProximos"''', re.S)
color_block_new = '''      <details class="card collapsible-card" id="colorVariantsCard">\n        <summary>\n          <div><strong>Gestionar variantes de color</strong><span>Solo para productos que realmente se venden en más de un color.</span></div>\n        </summary>\n        <div class="collapsible-content">\n          <div id="colorVariantsMsg"></div>\n          <div class="row" style="align-items:flex-end; margin-bottom:10px;">\n            <div style="flex:2; min-width:220px;">\n              <label for="colorProductSelect">Producto</label>\n              <select id="colorProductSelect" style="width:100%;"></select>\n            </div>\n            <div style="flex:1; min-width:150px;">\n              <label for="variantColorName">Nuevo color</label>\n              <input type="text" id="variantColorName" placeholder="Ej. Burgundy" style="margin-bottom:0;">\n            </div>\n            <div class="color-stock-field"><label>S</label><input type="number" min="0" id="variantColorS" value="0" style="width:64px; margin-bottom:0;"></div>\n            <div class="color-stock-field"><label>M</label><input type="number" min="0" id="variantColorM" value="0" style="width:64px; margin-bottom:0;"></div>\n            <div class="color-stock-field"><label>L</label><input type="number" min="0" id="variantColorL" value="0" style="width:64px; margin-bottom:0;"></div>\n            <div class="color-stock-field"><label>XL</label><input type="number" min="0" id="variantColorXL" value="0" style="width:64px; margin-bottom:0;"></div>\n            <button id="saveColorVariantBtn">Guardar color</button>\n          </div>\n          <div id="colorStockHint" class="color-mode-note hidden"></div>\n          <div class="table-scroll">\n            <table>\n              <thead id="colorVariantsHead"><tr><th>Color</th><th>S</th><th>M</th><th>L</th><th>XL</th><th>Total</th></tr></thead>\n              <tbody id="colorVariantsBody"></tbody>\n            </table>\n          </div>\n          <details class="advanced-details" style="margin-top:14px;">\n            <summary>Opciones avanzadas</summary>\n            <div class="details-body">\n              <button class="danger-ghost" id="disableColorVariantsBtn">Desactivar colores para este producto</button>\n              <p class="helper-text" style="margin-top:8px;">No borra los datos; solo vuelve temporalmente al stock tradicional por talla.</p>\n            </div>\n          </details>\n        </div>\n      </details>\n    </div>\n\n    <div id="viewProximos"'''
s, n = color_block_pattern.subn(color_block_new, s, count=1)
if n != 1:
    raise SystemExit(f'color manager block replace failed: {n}')

# ---------------------------------------------------------------------------
# 5) Upcoming drops: shorter instructions and collapse rare "new product" flow.
# ---------------------------------------------------------------------------
upcoming_copy = re.compile(r'''        <p class="sub" style="margin-bottom:14px;">\n          Prepara aquí el precio y las tallas de las prendas que aún no están en tu inventario\.\n          Cuando te lleguen, ponles precio y existencias y dale <strong>"Publicar"</strong> — aparecerán\n          automáticamente como "Disponible" en el catálogo público, sin que yo tenga que tocar código\.\n          Una vez publicada, la prenda desaparece de esta lista y pasa a manejarse desde\n          <strong>"Inventario"</strong> \(precio, tallas, y si quieres bajarla del catálogo\)\.\n        </p>''')
s, n = upcoming_copy.subn('''        <p class="section-intro">Prepara precio y stock. <strong>Guardar</strong> conserva el borrador; <strong>Publicar</strong> mueve la pieza al catálogo disponible y luego se administra desde Inventario.</p>''', s, count=1)
if n != 1:
    raise SystemExit(f'upcoming copy replace failed: {n}')

# Add a specific class to the upcoming table wrapper.
upcoming_marker = '''        <div id="upcomingMsg"></div>\n        <div class="table-scroll">'''
replace_once(upcoming_marker, '''        <div id="upcomingMsg"></div>\n        <div class="table-scroll upcoming-scroll">''', 'upcoming table wrapper')

# Merge the two low-frequency cards into one collapsed tool.
new_product_pattern = re.compile(r'''      <div class="card">\n        <h2>Agregar producto nuevo</h2>.*?      <div class="card">\n        <h2>Productos guardados sin foto todavía</h2>.*?      </div>\n    </div>\n  </div>''', re.S)
new_product_replacement = '''      <details class="card collapsible-card">\n        <summary>\n          <div><strong>Agregar producto fuera del catálogo</strong><span>Para una pieza nueva que todavía no tiene foto ni tarjeta pública.</span></div>\n        </summary>\n        <div class="collapsible-content">\n          <div id="newProductMsg"></div>\n          <div class="row" style="align-items:flex-end;">\n            <div style="flex:2; min-width:180px;">\n              <label for="newProductName">Nombre</label>\n              <input type="text" id="newProductName" placeholder="Ej. Kansas City Chiefs — Jersey Mahomes" style="margin-bottom:0;">\n            </div>\n            <div style="flex:1; min-width:120px;">\n              <label for="newProductCategory">Categoría</label>\n              <input type="text" id="newProductCategory" placeholder="T-shirt / Polo / Jacket" style="margin-bottom:0;">\n            </div>\n            <div style="flex:1; min-width:100px;">\n              <label for="newProductPrice">Precio</label>\n              <input type="number" min="0" step="0.01" id="newProductPrice" placeholder="$" style="margin-bottom:0;">\n            </div>\n          </div>\n          <div class="row" style="margin-top:12px; align-items:flex-end;">\n            <div><label>S</label><input type="number" min="0" id="newProductS" value="0" style="width:64px; margin-bottom:0;"></div>\n            <div><label>M</label><input type="number" min="0" id="newProductM" value="0" style="width:64px; margin-bottom:0;"></div>\n            <div><label>L</label><input type="number" min="0" id="newProductL" value="0" style="width:64px; margin-bottom:0;"></div>\n            <div><label>XL</label><input type="number" min="0" id="newProductXL" value="0" style="width:64px; margin-bottom:0;"></div>\n            <button id="newProductSaveBtn">Guardar borrador</button>\n          </div>\n          <p class="helper-text" style="margin-top:10px;">Guardar aquí no publica la pieza. Cuando tenga foto/tarjeta, podrá incorporarse al catálogo.</p>\n\n          <div class="subsection-title">Borradores sin foto</div>\n          <div id="draftsMsg"></div>\n          <div class="table-scroll">\n            <table>\n              <thead><tr><th>Producto</th><th>Categoría</th><th>Precio</th><th>S</th><th>M</th><th>L</th><th>XL</th><th></th></tr></thead>\n              <tbody id="draftsBody"></tbody>\n            </table>\n          </div>\n        </div>\n      </details>\n    </div>\n  </div>'''
s, n = new_product_pattern.subn(new_product_replacement, s, count=1)
if n != 1:
    raise SystemExit(f'new product block replace failed: {n}')

# ---------------------------------------------------------------------------
# 6) JS polish: friendlier labels, correct shared-size inventory, color UX.
# ---------------------------------------------------------------------------
# Add color mapping helper after money formatter.
replace_once(
'''  function moneyFmt(n) { return '$' + Number(n).toFixed(2); }''',
'''  function moneyFmt(n) { return '$' + Number(n).toFixed(2); }\n\n  function colorHexForName(name) {\n    const key = String(name || '').trim().toLowerCase();\n    const known = {\n      'burgundy': '#7B1E3A',\n      'berenjena': '#5A2B55',\n      'azul marino': '#19324F'\n    };\n    return known[key] || '#D9D9D6';\n  }''',
'color helper')

# Inventory calculations: shared color stock uses the legacy per-size stock, not
# the duplicated color rows. This fixes Adidas displaying 3x its real stock.
old_inventory_calc = '''      const colorVariants = p.product_color_variants || [];\n      const colorTotalBySize = {};\n      SIZE_ORDER.forEach(size => { colorTotalBySize[size] = colorVariants.filter(v => v.size === size).reduce((sum, v) => sum + v.stock_on_hand, 0); });\n      const total = p.uses_color_variants\n        ? SIZE_ORDER.reduce((sum, s) => sum + colorTotalBySize[s], 0)\n        : SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);\n\n      const tr = document.createElement('tr');\n      const sizeCells = SIZE_ORDER.map(s => {\n        if (p.uses_color_variants) return `<td>${colorTotalBySize[s]}</td>`;\n        const v = variants[s];\n        if (!v) return '<td>—</td>';\n        return `<td><input type="number" min="0" class="stock-input" data-variant-id="${v.id}" value="${v.stock_on_hand}"></td>`;\n      }).join('');'''
new_inventory_calc = '''      const colorVariants = p.product_color_variants || [];\n      const colorTotalBySize = {};\n      SIZE_ORDER.forEach(size => { colorTotalBySize[size] = colorVariants.filter(v => v.size === size).reduce((sum, v) => sum + v.stock_on_hand, 0); });\n      const sharedColorStock = p.uses_color_variants && p.color_stock_mode === 'shared_size';\n      const total = p.uses_color_variants && !sharedColorStock\n        ? SIZE_ORDER.reduce((sum, s) => sum + colorTotalBySize[s], 0)\n        : SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);\n\n      const tr = document.createElement('tr');\n      const sizeCells = SIZE_ORDER.map(s => {\n        if (p.uses_color_variants && !sharedColorStock) return `<td>${colorTotalBySize[s]}</td>`;\n        const v = variants[s];\n        if (!v) return '<td>—</td>';\n        return `<td><input type="number" min="0" class="stock-input" data-variant-id="${v.id}" value="${v.stock_on_hand}"></td>`;\n      }).join('');'''
replace_once(old_inventory_calc, new_inventory_calc, 'inventory shared stock')

old_inventory_row = '''      let statusLabel = p.sale_mode === 'preorder' ? 'Por encargo' : (total <= 0 ? '<span class="low-stock">Agotado</span>' : (total === 1 ? '<span class="low-stock">Última unidad</span>' : 'Disponible'));\n      const catalogBadge = p.active\n        ? '<span class="badge badge-paid">Publicado</span>'\n        : '<span class="badge badge-cancelled">Oculto</span>';\n\n      tr.innerHTML = `\n        <td>${p.name}${p.uses_color_variants ? ' <span class="badge badge-full">Colores</span>' : ''}</td>\n        <td><input type="number" min="0" step="0.01" class="stock-input" data-price-input value="${p.regular_price ?? ''}" placeholder="$"></td>\n        ${sizeCells}\n        <td>${total}</td>\n        <td>${statusLabel}</td>\n        <td>${catalogBadge}</td>\n        <td class="row" style="gap:6px; flex-wrap:nowrap;">\n          <button class="secondary save-stock-btn" data-product-id="${p.id}">${p.uses_color_variants ? 'Guardar precio' : 'Guardar'}</button>\n          <button class="secondary edit-colors-btn" data-product-id="${p.id}">Colores</button>\n          <button class="${p.active ? 'danger' : 'secondary'} toggle-active-btn" data-product-id="${p.id}" data-active="${p.active ? '1' : '0'}" data-name="${p.name}" title="${p.active ? 'Bajar del catálogo público' : 'Publicar en el catálogo público'}">${p.active ? 'Bajar' : 'Publicar'}</button>\n        </td>\n      `;'''
new_inventory_row = '''      let statusLabel = p.sale_mode === 'preorder'\n        ? '<span class="stock-state">Por encargo</span>'\n        : total <= 0\n          ? '<span class="stock-state stock-low">Agotado</span>'\n          : total === 1\n            ? '<span class="stock-state stock-low">Última unidad</span>'\n            : '<span class="stock-state stock-ok">Disponible</span>';\n      const catalogBadge = p.active\n        ? '<span class="badge badge-paid">Publicado</span>'\n        : '<span class="badge badge-cancelled">Oculto</span>';\n      const colorBadge = p.uses_color_variants\n        ? ` <span class="badge badge-full">${sharedColorStock ? '3 colores · stock compartido' : 'Colores'}</span>`\n        : '';\n      const colorAction = p.uses_color_variants\n        ? `<button class="secondary edit-colors-btn" data-product-id="${p.id}">Colores</button>`\n        : '';\n\n      tr.innerHTML = `\n        <td>${p.name}${colorBadge}</td>\n        <td><input type="number" min="0" step="0.01" class="stock-input" data-price-input value="${p.regular_price ?? ''}" placeholder="$"></td>\n        ${sizeCells}\n        <td><strong>${total}</strong></td>\n        <td>${statusLabel}</td>\n        <td>${catalogBadge}</td>\n        <td><div class="actions-cell">\n          <button class="secondary save-stock-btn" data-product-id="${p.id}">Guardar</button>\n          ${colorAction}\n          <button class="${p.active ? 'danger-ghost' : 'secondary'} toggle-active-btn" data-product-id="${p.id}" data-active="${p.active ? '1' : '0'}" data-name="${p.name}" title="${p.active ? 'Ocultar del catálogo público' : 'Publicar en el catálogo público'}">${p.active ? 'Ocultar' : 'Publicar'}</button>\n        </div></td>\n      `;'''
replace_once(old_inventory_row, new_inventory_row, 'inventory row')

# Make direct color action automatically expand the collapsed color manager.
replace_once(
'''      const select = document.getElementById('colorProductSelect');\n      select.value = editColorsBtn.dataset.productId;\n      await loadColorVariants();\n      document.getElementById('colorVariantsCard').scrollIntoView({ behavior: 'smooth', block: 'start' });''',
'''      const select = document.getElementById('colorProductSelect');\n      const colorCard = document.getElementById('colorVariantsCard');\n      colorCard.open = true;\n      select.value = editColorsBtn.dataset.productId;\n      await loadColorVariants();\n      colorCard.scrollIntoView({ behavior: 'smooth', block: 'start' });''',
'edit colors action')

# Replace color loader to understand shared-size mode and show friendly swatches.
color_loader_pattern = re.compile(r'''  async function loadColorVariants\(\) \{.*?\n  \}\n\n  document\.getElementById\('colorProductSelect'\)\.addEventListener\('change', loadColorVariants\);''', re.S)
color_loader_new = r'''  async function loadColorVariants() {
    const productId = document.getElementById('colorProductSelect').value;
    const tbody = document.getElementById('colorVariantsBody');
    const head = document.getElementById('colorVariantsHead');
    const hint = document.getElementById('colorStockHint');
    const msgEl = document.getElementById('colorVariantsMsg');
    tbody.innerHTML = '';
    showMsg(msgEl, '', null);
    if (!productId) return;

    const { data: productMeta, error: metaError } = await client.from('products')
      .select('color_stock_mode, product_variants(size, stock_on_hand)')
      .eq('id', productId)
      .single();
    if (metaError) { showMsg(msgEl, 'Error cargando configuración: ' + metaError.message, 'error'); return; }

    const shared = productMeta.color_stock_mode === 'shared_size';
    const baseStocks = {};
    (productMeta.product_variants || []).forEach(v => { baseStocks[v.size] = v.stock_on_hand; });
    SIZE_ORDER.forEach(size => {
      const input = document.getElementById('variantColor' + size);
      input.disabled = shared;
      if (shared) input.value = baseStocks[size] ?? 0;
    });
    hint.classList.toggle('hidden', !shared);
    hint.textContent = shared
      ? `Este producto usa stock compartido por talla: ${SIZE_ORDER.map(s => `${s} ${baseStocks[s] ?? 0}`).join(' · ')}. Los colores son una elección visual y no multiplican las unidades.`
      : '';

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
      head.innerHTML = '<tr><th>Color</th><th>Inventario</th></tr>';
      tbody.innerHTML = '<tr><td colspan="2" style="color:var(--ink-soft);">Este producto todavía no tiene colores configurados.</td></tr>';
      return;
    }

    if (shared) {
      head.innerHTML = '<tr><th>Color</th><th>Inventario</th></tr>';
      const stockSummary = SIZE_ORDER.map(s => `${s} ${baseStocks[s] ?? 0}`).join(' · ');
      colors.forEach(color => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td><span class="color-dot" style="background:${colorHexForName(color)}"></span>${color}</td><td><span class="badge badge-full">Stock compartido</span> <span class="helper-text">${stockSummary}</span></td>`;
        tbody.appendChild(tr);
      });
      return;
    }

    head.innerHTML = '<tr><th>Color</th><th>S</th><th>M</th><th>L</th><th>XL</th><th>Total</th></tr>';
    colors.forEach(color => {
      const total = SIZE_ORDER.reduce((sum, size) => sum + (grouped[color][size]?.stock_on_hand || 0), 0);
      const tr = document.createElement('tr');
      tr.innerHTML = `<td><span class="color-dot" style="background:${colorHexForName(color)}"></span>${color}</td>${SIZE_ORDER.map(size => `<td>${grouped[color][size]?.stock_on_hand ?? 0}</td>`).join('')}<td><strong>${total}</strong></td>`;
      tbody.appendChild(tr);
    });
  }

  document.getElementById('colorProductSelect').addEventListener('change', loadColorVariants);'''
s, n = color_loader_pattern.subn(color_loader_new, s, count=1)
if n != 1:
    raise SystemExit(f'color loader replace failed: {n}')

# Shorter upcoming statuses.
replace_once("${isSaved ? 'Guardado, sin publicar' : 'Sin publicar'}", "${isSaved ? 'Borrador' : 'Pendiente'}", 'upcoming status label')

# Friendlier cancel action label in reservations while preserving behavior.
s = s.replace('Cancelar / liberar stock', 'Cancelar reserva')

# Validation
required = [
    'point12-panel-polish',
    'PRIME DROP / OPERATIONS',
    'Cómo funciona una reserva con abono 50%',
    'Exportar solicitudes',
    'Gestionar variantes de color',
    'Agregar producto fuera del catálogo',
    "const sharedColorStock = p.uses_color_variants && p.color_stock_mode === 'shared_size';",
    '3 colores · stock compartido',
    'colorStockHint',
    'Stock compartido',
    "${isSaved ? 'Borrador' : 'Pendiente'}"
]
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit(f'Point 12 visual validation failed: {missing}')

if s == original:
    raise SystemExit('No visual changes produced')
path.write_text(s, encoding='utf-8')
