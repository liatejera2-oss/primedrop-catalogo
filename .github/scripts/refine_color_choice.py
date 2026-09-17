from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

pairs = [
(".select('id, slug, name, regular_price, preorder_price, sale_mode, active, uses_color_variants, product_variants(id, size, stock_on_hand), product_color_variants(id, color, size, stock_on_hand)')",
 ".select('id, slug, name, regular_price, preorder_price, sale_mode, active, uses_color_variants, color_stock_mode, product_variants(id, size, stock_on_hand), product_color_variants(id, color, size, stock_on_hand)')"),
("""    function totalStock(product) {
      if (product.uses_color_variants && product.colors && product.colors.length) {
        return product.colors.reduce((sum, color) => sum + SIZE_ORDER.reduce((inner, size) => {
          const variant = product.colorVariants[color]?.[size];
          return inner + (variant ? variant.stock_on_hand : 0);
        }, 0), 0);
      }
      return SIZE_ORDER.reduce((sum, s) => sum + (product.variants[s] ? product.variants[s].stock_on_hand : 0), 0);
    }
""",
"""    function totalStock(product) {
      if (product.uses_color_variants && product.color_stock_mode !== 'shared_size' && product.colors && product.colors.length) {
        return product.colors.reduce((sum, color) => sum + SIZE_ORDER.reduce((inner, size) => {
          const variant = product.colorVariants[color]?.[size];
          return inner + (variant ? variant.stock_on_hand : 0);
        }, 0), 0);
      }
      return SIZE_ORDER.reduce((sum, s) => sum + (product.variants[s] ? product.variants[s].stock_on_hand : 0), 0);
    }
"""),
("""    function stockForSelection(product, size, color = null) {
      if (product.uses_color_variants && product.colors && product.colors.length) {
        if (color) return product.colorVariants[color]?.[size]?.stock_on_hand ?? 0;
        return product.colors.reduce((sum, c) => sum + (product.colorVariants[c]?.[size]?.stock_on_hand ?? 0), 0);
      }
      return product.variants[size]?.stock_on_hand ?? 0;
    }
""",
"""    function stockForSelection(product, size, color = null) {
      if (product.uses_color_variants && product.color_stock_mode === 'shared_size') {
        return product.variants[size]?.stock_on_hand ?? 0;
      }
      if (product.uses_color_variants && product.colors && product.colors.length) {
        if (color) return product.colorVariants[color]?.[size]?.stock_on_hand ?? 0;
        return product.colors.reduce((sum, c) => sum + (product.colorVariants[c]?.[size]?.stock_on_hand ?? 0), 0);
      }
      return product.variants[size]?.stock_on_hand ?? 0;
    }
"""),
("""  .purchase-color-btn { font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; min-height: 40px; padding: 0 14px; border-radius: 6px; border: 1px solid var(--line); background: #fff; color: var(--ink); cursor: pointer; transition: border-color .15s ease, background .15s ease; }
  .purchase-color-btn[aria-pressed=\"true\"] { background: var(--ink); border-color: var(--ink); color: #fff; }
""",
"""  .purchase-color-btn { font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; min-height: 44px; min-width: 104px; padding: 0 14px; border-radius: 8px; border: 1px solid var(--line); background: #fff; color: var(--ink); cursor: pointer; transition: border-color .15s ease, background .15s ease, box-shadow .15s ease; }
  .purchase-color-btn:hover { border-color: #9ca3af; }
  .purchase-color-btn[aria-pressed=\"true\"] { background: var(--ink); border-color: var(--ink); color: #fff; box-shadow: 0 0 0 2px rgba(17,24,39,.08); }
""")
]
for old,new in pairs:
    if old not in s:
        raise SystemExit('Missing index anchor: ' + old[:80])
    s = s.replace(old,new,1)
p.write_text(s, encoding='utf-8')

p = Path('panel-privado.html')
s = p.read_text(encoding='utf-8')
old = ".select('id, slug, name, sale_mode, regular_price, active, published_once, uses_color_variants, product_variants(id, size, stock_on_hand), product_color_variants(id, color, size, stock_on_hand)')"
if old in s:
    s = s.replace(old, ".select('id, slug, name, sale_mode, regular_price, active, published_once, uses_color_variants, color_stock_mode, product_variants(id, size, stock_on_hand), product_color_variants(id, color, size, stock_on_hand)')", 1)
old = """      const total = p.uses_color_variants
        ? (p.product_color_variants || []).reduce((sum, v) => sum + v.stock_on_hand, 0)
        : SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);
"""
new = """      const total = p.uses_color_variants && p.color_stock_mode !== 'shared_size'
        ? (p.product_color_variants || []).reduce((sum, v) => sum + v.stock_on_hand, 0)
        : SIZE_ORDER.reduce((sum, s) => sum + (variants[s] ? variants[s].stock_on_hand : 0), 0);
"""
if old in s:
    s = s.replace(old,new,1)
p.write_text(s, encoding='utf-8')
