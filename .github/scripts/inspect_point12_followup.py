from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
patterns=['async function loadCatalog','function colorStyleFor','function renderColorOptions','data-product="barca-morado-yamal"','get_published_product_states','product_name','querySelector(\'.product-name\'','product-title']
for pat in patterns:
    print('\n###',pat)
    i=s.find(pat)
    print('index',i)
    if i>=0:
        print(s[max(0,i-1200):i+3500])
