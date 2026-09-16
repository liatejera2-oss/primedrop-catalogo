from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
original = html

old_breakpoint = "@media (max-width: 700px) {\n    .header-inner { position: relative; flex-wrap: nowrap; }"
new_breakpoint = "@media (max-width: 768px) {\n    .header-inner { position: relative; flex-wrap: nowrap; }"
if old_breakpoint not in html:
    raise SystemExit('Header mobile breakpoint block not found; aborting.')
html = html.replace(old_breakpoint, new_breakpoint, 1)

old_shadow = "box-shadow: 0 16px 38px rgba(17,17,17,.10);"
if old_shadow not in html:
    raise SystemExit('Header mobile shadow not found; aborting.')
html = html.replace(old_shadow, '', 1)

old_resize = "if (window.innerWidth > 700) setOpen(false);"
new_resize = "if (window.innerWidth > 768) setOpen(false);"
if old_resize not in html:
    raise SystemExit('Header resize breakpoint not found; aborting.')
html = html.replace(old_resize, new_resize, 1)

checks = [
    "@media (max-width: 768px) {\n    .header-inner { position: relative; flex-wrap: nowrap; }",
    "if (window.innerWidth > 768) setOpen(false);",
    "href=\"#upcomingSectionHead\">Próximos Drops</a>",
    "href=\"https://www.instagram.com/primedrop.pa/\"",
    ">Comprar por Instagram ↗</a>",
]
missing = [item for item in checks if item not in html]
if missing:
    raise SystemExit(f'Post-change validation failed: {missing}')
if old_shadow in html:
    raise SystemExit('Header shadow still present after replacement.')
if html == original:
    raise SystemExit('No changes produced; aborting.')

path.write_text(html, encoding='utf-8')
