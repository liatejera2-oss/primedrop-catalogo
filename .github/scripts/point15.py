from pathlib import Path
import base64, hashlib, re

html_path = Path('index.html')
s = html_path.read_text(encoding='utf-8')
out_dir = Path('assets/media')
out_dir.mkdir(parents=True, exist_ok=True)

pattern = re.compile(r'data:image/(png|jpe?g|webp|gif);base64,([A-Za-z0-9+/=\r\n]+)', re.I)
created = {}
bytes_written = 0

def repl(match):
    global bytes_written
    mime = match.group(1).lower()
    payload = re.sub(r'\s+', '', match.group(2))
    raw = base64.b64decode(payload)
    digest = hashlib.sha256(raw).hexdigest()[:16]
    ext = 'jpg' if mime in ('jpeg','jpg') else mime
    rel = f'assets/media/{digest}.{ext}'
    path = Path(rel)
    if rel not in created:
        path.write_bytes(raw)
        created[rel] = len(raw)
        bytes_written += len(raw)
    return rel

s, count = pattern.subn(repl, s)
if count == 0:
    raise SystemExit('No embedded images found; performance extraction did not run')

# Let the browser decode images off the main rendering path. Keep the hero high priority.
s = re.sub(r'<img(?![^>]*\bdecoding=)([^>]*?)>', r'<img\1 decoding="async">', s)
s = s.replace('class="hero-bag"', 'class="hero-bag" fetchpriority="high"', 1)

# Security/performance hint for the Supabase CDN script if present: defer parsing until HTML is available.
s = s.replace('<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js" defer></script>', 1)

html_path.write_text(s, encoding='utf-8')
print(f'extracted_occurrences={count}')
print(f'unique_assets={len(created)}')
print(f'binary_bytes={bytes_written}')
print(f'html_bytes={html_path.stat().st_size}')
