from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
original = html

old_css = '''  .upcoming-card .price { font-size: 14px; font-weight: 500; color: var(--ink-soft); letter-spacing: 0; }
  .upcoming-card .size-row { margin-bottom: 0; }

  .upcoming-section { max-width: 1200px; margin: 0 auto; padding: 0 24px var(--space-7); }
  .upcoming-intro { font-size: 14px; color: var(--ink-soft); max-width: 520px; margin: -10px 0 var(--space-3); line-height: 1.55; font-weight: 400; }
'''
new_css = '''  .upcoming-card .price { font-size: 14px; font-weight: 500; color: var(--ink-soft); letter-spacing: 0; }
  .upcoming-card .size-row { display: none; }

  .upcoming-head { align-items: center; }
  .upcoming-instagram-link { display: inline-flex; align-items: center; min-height: 40px; padding: 8px 14px; border: 1px solid var(--line); border-radius: var(--radius-pill); font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; color: var(--ink); text-decoration: none; background: #fff; white-space: nowrap; transition: background .2s ease, border-color .2s ease; }
  .upcoming-instagram-link:hover, .upcoming-instagram-link:focus-visible { background: var(--bg-alt); border-color: #D5D5D8; }
  .upcoming-section { max-width: 1200px; margin: 0 auto; padding: 0 24px var(--space-7); }
  .upcoming-grid { display: flex; gap: 20px; overflow-x: auto; max-width: 100%; padding: 2px 2px 14px; scroll-snap-type: x proximity; scroll-padding-left: 2px; overscroll-behavior-x: contain; -webkit-overflow-scrolling: touch; scrollbar-width: thin; scrollbar-color: #D5D5D8 transparent; }
  .upcoming-grid .upcoming-card { flex: 0 0 clamp(280px, 31%, 354px); scroll-snap-align: start; }
  .upcoming-grid::-webkit-scrollbar { height: 5px; }
  .upcoming-grid::-webkit-scrollbar-track { background: transparent; }
  .upcoming-grid::-webkit-scrollbar-thumb { background: #D5D5D8; border-radius: var(--radius-pill); }
  @media (max-width: 600px) {
    .upcoming-head .upcoming-instagram-link { margin-top: 14px; min-height: 44px; width: 100%; justify-content: center; }
    .upcoming-grid { margin-right: -16px; padding-right: 16px; gap: 14px; scrollbar-width: none; }
    .upcoming-grid::-webkit-scrollbar { display: none; }
    .upcoming-grid .upcoming-card { flex-basis: min(82vw, 320px); }
  }
'''
if old_css not in html:
    raise SystemExit('Expected upcoming CSS block not found')
html = html.replace(old_css, new_css, 1)

old_html = '''<div class="section-head" id="upcomingSectionHead">
  <div class="section-title">Próximos Drops</div>
</div>
<section class="upcoming-section" id="upcomingSection">
  <p class="upcoming-intro">Nuevos drops se incorporarán al catálogo. Síguenos en Instagram para conocer primero cada lanzamiento.</p>
  <div class="grid">
'''
new_html = '''<div class="section-head upcoming-head" id="upcomingSectionHead">
  <div class="section-title">Próximos Drops<span>Anticipa los próximos lanzamientos. Cuando una pieza esté disponible, la encontrarás arriba en el catálogo.</span></div>
  <a class="upcoming-instagram-link" href="https://www.instagram.com/primedrop.pa/" target="_blank" rel="noopener noreferrer">Seguir @primedrop.pa ↗</a>
</div>
<section class="upcoming-section" id="upcomingSection" aria-label="Próximos Drops">
  <div class="grid upcoming-grid">
'''
if old_html not in html:
    raise SystemExit('Expected upcoming section header not found')
html = html.replace(old_html, new_html, 1)

old_move = '''        card.classList.remove('upcoming-card');
        if (!card.dataset.cat) card.dataset.cat = 'jerseys'; // los 7 próximos drops actuales son jerseys de fútbol
        mainGrid.appendChild(card);
        moved = true;
'''
new_move = '''        card.classList.remove('upcoming-card');
        tag.classList.remove('status-soon');
        if (!card.dataset.cat) card.dataset.cat = 'jerseys'; // los 7 próximos drops actuales son jerseys de fútbol
        mainGrid.appendChild(card);
        moved = true;
'''
if old_move not in html:
    raise SystemExit('Expected upcoming migration block not found')
html = html.replace(old_move, new_move, 1)

required = [
    'class="section-head upcoming-head"',
    'Seguir @primedrop.pa ↗',
    'class="grid upcoming-grid"',
    '.upcoming-grid .upcoming-card { flex:',
    '.upcoming-card .size-row { display: none; }',
    "tag.classList.remove('status-soon');",
    'migrateUpcomingCards();',
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit(f'Upcoming validation failed: {missing}')

if html == original:
    raise SystemExit('No upcoming changes produced')

path.write_text(html, encoding='utf-8')
