from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

# Print a bounded excerpt around the first hero-related markup without exposing embedded base64 assets.
patterns = [
    r'<[^>]+class="[^"]*hero-wrap[^"]*"[^>]*>',
    r'<[^>]+class="[^"]*hero[^"]*"[^>]*>',
    r'<section[^>]*class="[^"]*hero[^"]*"[^>]*>',
]
start = None
for pattern in patterns:
    m = re.search(pattern, html, re.I)
    if m:
        start = max(0, m.start() - 400)
        break

if start is None:
    raise SystemExit('Hero markup not found')

excerpt = html[start:start + 7000]
# Remove data URLs/base64 payloads if one happens to fall inside the excerpt.
excerpt = re.sub(r'data:[^\"\']+;base64,[A-Za-z0-9+/=\s]+', 'data:[embedded-image-omitted]', excerpt)
print('=== HERO MARKUP EXCERPT ===')
print(excerpt)

print('\n=== HERO CSS RULES ===')
style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, flags=re.I | re.S)
for block in style_blocks:
    for line in block.splitlines():
        if '.hero' in line or 'hero-' in line:
            print(line.strip())
