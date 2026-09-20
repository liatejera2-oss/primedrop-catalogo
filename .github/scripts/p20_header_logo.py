from pathlib import Path
p=Path("index.html")
s=p.read_text(encoding="utf-8")

old_css=".brand img { width: 38px; height: 38px; border-radius: 50%; object-fit: cover; border: 1px solid var(--line); }"
new_css=".brand img { width: 48px; height: 48px; border-radius: 50%; object-fit: cover; border: 1px solid var(--line); flex: 0 0 48px; }"
assert old_css in s
s=s.replace(old_css,new_css,1)

mobile_anchor="""  @media (max-width: 768px) {
    .header-inner { position: relative; flex-wrap: nowrap; }
"""
mobile_new="""  @media (max-width: 768px) {
    .header-inner { position: relative; flex-wrap: nowrap; }
    .brand img { width: 40px; height: 40px; flex-basis: 40px; }
"""
assert mobile_anchor in s
s=s.replace(mobile_anchor,mobile_new,1)

old_img='<img src="assets/media/9336c0169971d6ae.jpg" alt="Prime Drop logo" width="38" height="38" decoding="async">'
new_img='<img src="assets/media/9336c0169971d6ae.jpg" alt="Prime Drop logo" width="48" height="48" decoding="async">'
assert old_img in s
s=s.replace(old_img,new_img,1)

p.write_text(s,encoding="utf-8")
print("Header logo scaled to 48px desktop / 40px mobile")
