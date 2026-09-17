from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
original = html

old_grid = "@media (max-width: 600px) { .grid { grid-template-columns: 1fr; gap: 28px; } }"
new_grid = "@media (max-width: 600px) { .grid { grid-template-columns: 1fr; gap: 24px; } }"
if old_grid not in html:
    raise SystemExit('Expected mobile grid rule not found')
html = html.replace(old_grid, new_grid, 1)

old_block = '''@media (max-width: 600px) {
    .hero-wrap { margin: 0; padding: 0; }
    .hero { padding: 36px 20px 30px; border-radius: 0; }
    .hero-actions { flex-direction: column; align-items: stretch; gap: 14px; }
    .hero-cta-primary { width: 100%; }
    .hero-cta-secondary { text-align: center; }
    .hero-trust { text-align: center; }
    .header-inner { padding: 12px 16px; }
    .steps { grid-template-columns: 1fr; }
    .card-info h3 { font-size: 14.5px; }
    .price { font-size: 15px; }
  }'''

new_block = '''@media (max-width: 600px) {
    .hero-wrap { margin: 0; padding: 0; }
    .hero { padding: 32px 18px 28px; border-radius: 0; gap: 0; }
    .hero-eyebrow { font-size: 11.5px; margin-bottom: 14px; }
    .hero h1 { font-size: clamp(30px, 9vw, 36px); line-height: 1.08; letter-spacing: -0.028em; }
    .hero-sub { margin-top: 14px; font-size: 15px; line-height: 1.55; }
    .hero-actions { margin-top: 24px; flex-direction: column; align-items: stretch; gap: 10px; }
    .hero-cta-primary { width: 100%; min-height: 48px; padding: 13px 20px; }
    .hero-cta-secondary { display: inline-flex; align-items: center; justify-content: center; width: 100%; min-height: 46px; padding: 11px 18px; text-align: center; border: 1px solid var(--line); border-radius: var(--radius-pill); }
    .hero-trust { margin-top: 20px; text-align: center; font-size: 11.5px; line-height: 1.6; }
    .hero-visual { padding-top: 22px; }
    .hero-bag { width: 170px; }

    .header-inner { padding: 12px 16px; }

    .section-head { display: block; padding: 0 16px; margin-bottom: 20px; }
    .section-title { font-size: 20px; line-height: 1.2; }
    .section-title span { margin-top: 6px; font-size: 13.5px; line-height: 1.5; }
    .filters { width: 100%; margin-top: 16px; padding: 2px 0 5px; }
    .filter-btn { min-height: 44px; padding: 9px 14px; }

    .catalog, .upcoming-section, .how-to-buy { padding-left: 16px; padding-right: 16px; }
    .upcoming-intro { margin-top: -6px; font-size: 13.5px; line-height: 1.55; }

    .card { transform: none; }
    .card:hover { transform: none; box-shadow: none; }
    .card-media > img, .slide img { padding: 18px; }
    .card:hover .slide img, .card:hover .card-media > img { transform: none; }
    .status-tag { top: 10px; left: 10px; }
    .dots { bottom: 8px; opacity: 1; pointer-events: auto; }
    .dot-btn { width: 7px; height: 7px; }
    .dot-btn.active { width: 16px; }
    .card-info { padding: 18px; }
    .card-info h3 { font-size: 17px; line-height: 1.28; margin-bottom: 9px; }
    .price { font-size: 16px; }
    .size-row { margin-top: 14px; margin-bottom: 14px; }
    .ig-btn { min-height: 48px; }

    .steps { grid-template-columns: 1fr; gap: 12px; }
    .how-to-buy h2 { font-size: 18px; margin-bottom: 16px; }
    .step { padding: 18px; }

    footer { padding: 28px 16px; }
    .footer-inner { flex-direction: column; align-items: stretch; gap: 14px; }
    .footer-inner p { line-height: 1.5; }
    .footer-inner a { display: inline-flex; align-items: center; justify-content: center; min-height: 44px; width: 100%; }
  }'''

if old_block not in html:
    raise SystemExit('Expected primary mobile block not found')
html = html.replace(old_block, new_block, 1)

required = [
    '.hero h1 { font-size: clamp(30px, 9vw, 36px);',
    '.section-head { display: block; padding: 0 16px;',
    '.filter-btn { min-height: 44px;',
    '.catalog, .upcoming-section, .how-to-buy { padding-left: 16px;',
    '.dots { bottom: 8px; opacity: 1; pointer-events: auto; }',
    '.card-info h3 { font-size: 17px;',
    '.ig-btn { min-height: 48px; }',
    '.footer-inner { flex-direction: column; align-items: stretch;',
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit(f'Mobile validation failed: {missing}')

if html == original:
    raise SystemExit('No mobile changes produced')

path.write_text(html, encoding='utf-8')
