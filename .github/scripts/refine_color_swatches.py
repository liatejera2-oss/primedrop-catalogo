from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_css = """  .purchase-color-btn { font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; min-height: 44px; min-width: 104px; padding: 0 14px; border-radius: 8px; border: 1px solid var(--line); background: #fff; color: var(--ink); cursor: pointer; transition: border-color .15s ease, background .15s ease, box-shadow .15s ease; }
  .purchase-color-btn:hover { border-color: #9ca3af; }
  .purchase-color-btn[aria-pressed=\"true\"] { background: var(--ink); border-color: var(--ink); color: #fff; box-shadow: 0 0 0 2px rgba(17,24,39,.08); }
"""
new_css = """  .purchase-color-btn { position: relative; width: 46px; height: 46px; min-width: 46px; padding: 0; border-radius: 8px; border: 1px solid rgba(17,24,39,.18); background: var(--swatch, #fff); cursor: pointer; transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease; }
  .purchase-color-btn:hover { transform: translateY(-1px); border-color: rgba(17,24,39,.42); }
  .purchase-color-btn:focus-visible { outline: 2px solid var(--ink); outline-offset: 3px; }
  .purchase-color-btn[aria-pressed=\"true\"] { border-color: transparent; box-shadow: 0 0 0 2px #fff, 0 0 0 4px var(--ink); }
  .purchase-color-btn[aria-pressed=\"true\"]::after { content: '✓'; position: absolute; inset: 0; display: grid; place-items: center; color: #fff; font-size: 17px; font-weight: 800; text-shadow: 0 1px 2px rgba(0,0,0,.4); }
"""
if old_css not in s:
    raise SystemExit('color CSS anchor missing')
s = s.replace(old_css, new_css, 1)

old_render = """      colorsEl.innerHTML = hasColors ? product.colors.map(color =>
        `<button type=\"button\" class=\"purchase-color-btn\" data-color=\"${color}\" aria-pressed=\"false\">${color}</button>`
      ).join('') : '';
"""
new_render = """      const COLOR_SWATCHES = {
        'Burgundy': '#7B1E3A',
        'Berenjena': '#4B2647',
        'Azul marino': '#172A46'
      };
      colorsEl.innerHTML = hasColors ? product.colors.map(color => {
        const swatch = COLOR_SWATCHES[color] || '#6B7280';
        return `<button type=\"button\" class=\"purchase-color-btn\" data-color=\"${color}\" aria-label=\"${color}\" title=\"${color}\" aria-pressed=\"false\" style=\"--swatch:${swatch}\"></button>`;
      }).join('') : '';
"""
if old_render not in s:
    raise SystemExit('color render anchor missing')
s = s.replace(old_render, new_render, 1)

required = [
    "'Burgundy': '#7B1E3A'",
    "'Berenjena': '#4B2647'",
    "'Azul marino': '#172A46'",
    'aria-label=\"${color}\"',
    "content: '✓'",
]
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit(f'validation failed: {missing}')

p.write_text(s, encoding='utf-8')
