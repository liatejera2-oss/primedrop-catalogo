from pathlib import Path
import re

p = Path('panel-privado.html')
s = p.read_text(encoding='utf-8')

css_anchor = "  .inventory-note strong { color:var(--ink); }\n"
css_add = css_anchor + """  .inventory-overview { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin:0 0 14px; }
  .inventory-metric { border:1px solid var(--panel-line); border-radius:12px; background:#fff; padding:12px 14px; }
  .inventory-metric span { display:block; color:var(--ink-soft); font-size:10.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; margin-bottom:5px; }
  .inventory-metric strong { font-size:20px; letter-spacing:-.02em; }
  .inventory-filters { display:flex; gap:6px; flex-wrap:wrap; margin:0 0 14px; }
  .inventory-filter-btn { background:transparent; color:var(--ink-soft); border:1px solid var(--panel-line); min-height:34px; padding:6px 12px; }
  .inventory-filter-btn.active { background:var(--panel-muted); color:var(--ink); border-color:var(--panel-line); }
  .inventory-filter-status { min-height:18px; color:var(--ink-soft); font-size:12px; margin:-4px 0 10px; }
  @media (max-width:760px) { .inventory-overview { grid-template-columns:repeat(2,minmax(0,1fr)); } }
"""
assert css_anchor in s, 'inventory CSS anchor missing'
s = s.replace(css_anchor, css_add, 1)

html_anchor = '''        <div class="inventory-note"><span>ⓘ</span><span><strong>Catálogo</strong> solo controla si la pieza se ve públicamente. Ocultarla no elimina su inventario.</span></div>
        <div id="inventoryMsg"></div>'''
html_repl = '''        <div class="inventory-note"><span>ⓘ</span><span><strong>Catálogo</strong> solo controla si la pieza se ve públicamente. Ocultarla no elimina su inventario.</span></div>
        <div class="inventory-overview" aria-label="Resumen de inventario">
          <div class="inventory-metric"><span>Unidades físicas</span><strong id="inventoryUnits">0</strong></div>
          <div class="inventory-metric"><span>Última unidad</span><strong id="inventoryLow">0</strong></div>
          <div class="inventory-metric"><span>Agotados</span><strong id="inventoryOut">0</strong></div>
          <div class="inventory-metric"><span>Ocultos</span><strong id="inventoryHidden">0</strong></div>
        </div>
        <div class="inventory-filters" id="inventoryFilters" role="group" aria-label="Filtrar inventario">
          <button class="inventory-filter-btn active" data-inventory-filter="all" aria-pressed="true">Todo</button>
          <button class="inventory-filter-btn" data-inventory-filter="low" aria-pressed="false">Última unidad</button>
          <button class="inventory-filter-btn" data-inventory-filter="out" aria-pressed="false">Agotados</button>
          <button class="inventory-filter-btn" data-inventory-filter="preorder" aria-pressed="false">Por encargo</button>
          <button class="inventory-filter-btn" data-inventory-filter="hidden" aria-pressed="false">Ocultos</button>
        </div>
        <div id="inventoryFilterStatus" class="inventory-filter-status" role="status" aria-live="polite"></div>
        <div id="inventoryMsg"></div>'''
assert html_anchor in s, 'inventory HTML anchor missing'
s = s.replace(html_anchor, html_repl, 1)

s = s.replace('<label for="variantColorName">Nuevo color</label>', '<label for="variantColorName">Color</label>', 1)
s = s.replace('<div><strong>Gestionar variantes de color</strong><span>Solo para productos que realmente se venden en más de un color.</span></div>', '<div><strong>Gestionar variantes de color</strong><span>Agrega un color nuevo o actualiza uno existente sin crear duplicados.</span></div>', 1)

size_anchor = "  const SIZE_ORDER = ['S', 'M', 'L', 'XL'];\n"
assert size_anchor in s
s = s.replace(size_anchor, size_anchor + "  let inventoryFilter = 'all';\n", 1)

inv_marker = "  // ---- Inventario ----\n  async function loadInventory() {\n"
inv_helpers = '''  // ---- Inventario ----
  function applyInventoryFilter() {
    const rows = Array.from(document.querySelectorAll('#inventoryBody tr[data-stock-state]'));
    let visible = 0;
    rows.forEach(tr => {
      const matches = inventoryFilter === 'all'
        || (inventoryFilter === 'hidden' && tr.dataset.active === '0')
        || tr.dataset.stockState === inventoryFilter;
      tr.hidden = !matches;
      if (matches) visible += 1;
    });
    const status = document.getElementById('inventoryFilterStatus');
    if (status) status.textContent = inventoryFilter === 'all' ? '' : `${visible} producto${visible === 1 ? '' : 's'} en este filtro.`;
  }

  const inventoryFilters = document.getElementById('inventoryFilters');
  if (inventoryFilters) inventoryFilters.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-inventory-filter]');
    if (!btn) return;
    inventoryFilter = btn.dataset.inventoryFilter;
    inventoryFilters.querySelectorAll('[data-inventory-filter]').forEach(b => {
      const active = b === btn;
      b.classList.toggle('active', active);
      b.setAttribute('aria-pressed', String(active));
    });
    applyInventoryFilter();
  });

  async function loadInventory() {
'''
assert inv_marker in s, 'inventory marker missing'
s = s.replace(inv_marker, inv_helpers, 1)

rows_anchor = "    const rows = data.filter(p => p.published_once || !upcomingSlugs.has(p.slug));\n\n    rows.forEach(p => {\n"
rows_repl = "    const rows = data.filter(p => p.published_once || !upcomingSlugs.has(p.slug));\n    let inventoryUnits = 0, inventoryLow = 0, inventoryOut = 0, inventoryHidden = 0;\n\n    rows.forEach(p => {\n"
assert rows_anchor in s, 'rows anchor missing'
s = s.replace(rows_anchor, rows_repl, 1)

total_anchor = """      const total = p.uses_color_variants && !sharedColorStock
        ? SIZE_ORDER.reduce((sum, s) => sum + colorTotalBySize[s], 0)
        : SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);

      const tr = document.createElement('tr');
"""
total_repl = """      const total = p.uses_color_variants && !sharedColorStock
        ? SIZE_ORDER.reduce((sum, s) => sum + colorTotalBySize[s], 0)
        : SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);
      const stockState = p.sale_mode === 'preorder' ? 'preorder' : total <= 0 ? 'out' : total === 1 ? 'low' : 'ok';
      inventoryUnits += total;
      if (stockState === 'low') inventoryLow += 1;
      if (stockState === 'out') inventoryOut += 1;
      if (!p.active) inventoryHidden += 1;

      const tr = document.createElement('tr');
      tr.dataset.stockState = stockState;
      tr.dataset.active = p.active ? '1' : '0';
      tr.dataset.productId = p.id;
"""
assert total_anchor in s, 'total anchor missing'
s = s.replace(total_anchor, total_repl, 1)

end_anchor = """      tbody.appendChild(tr);
    });
    await loadColorProductOptions();
  }
"""
end_repl = """      tbody.appendChild(tr);
    });
    document.getElementById('inventoryUnits').textContent = inventoryUnits;
    document.getElementById('inventoryLow').textContent = inventoryLow;
    document.getElementById('inventoryOut').textContent = inventoryOut;
    document.getElementById('inventoryHidden').textContent = inventoryHidden;
    applyInventoryFilter();
    await loadColorProductOptions();
  }
"""
assert end_anchor in s, 'inventory end anchor missing'
s = s.replace(end_anchor, end_repl, 1)

pattern = re.compile(r"  document\.getElementById\('saveColorVariantBtn'\)\.addEventListener\('click', async \(\) => \{.*?\n  \}\);\n\n  document\.getElementById\('disableColorVariantsBtn'\)", re.S)
match = pattern.search(s)
assert match, 'save color handler missing'
replacement = '''  document.getElementById('saveColorVariantBtn').addEventListener('click', async () => {
    const btn = document.getElementById('saveColorVariantBtn');
    const msgEl = document.getElementById('colorVariantsMsg');
    const productId = document.getElementById('colorProductSelect').value;
    const color = document.getElementById('variantColorName').value.trim();
    const stocks = {};
    SIZE_ORDER.forEach(size => {
      const input = document.getElementById('variantColor' + size);
      stocks[size] = Math.max(0, parseInt(input?.value, 10) || 0);
    });
    if (!productId || !color) { showMsg(msgEl, 'Selecciona un producto y escribe el color.', 'error'); return; }

    btn.disabled = true;
    const { data, error } = await client.rpc('save_product_color_stock', {
      p_product_id: productId,
      p_color: color,
      p_stocks: stocks
    });
    btn.disabled = false;
    if (error) { showMsg(msgEl, 'Error guardando color: ' + error.message, 'error'); return; }

    const row = Array.isArray(data) ? data[0] : data;
    document.getElementById('variantColorName').value = '';
    const shared = row?.stock_mode === 'shared_size';
    showMsg(msgEl, shared
      ? `Color "${row?.color || color}" guardado. Usa el stock general por talla; no se duplicaron unidades.`
      : `Color "${row?.color || color}" guardado. Si ya existía, se actualizó en lugar de crear un duplicado.`, 'ok');
    await loadColorVariants();
    await loadInventory();
  });

  document.getElementById('disableColorVariantsBtn')'''
s = s[:match.start()] + replacement + s[match.end():]

p.write_text(s, encoding='utf-8')
print('Point 14 patched')
