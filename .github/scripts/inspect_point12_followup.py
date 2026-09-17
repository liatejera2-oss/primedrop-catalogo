from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
patterns=['color-swatch','selectedColor','colorOptions','color-option','colorSwatch','colorStyles','Burgundy','function openPurchase','purchaseColor','modalColor','const COLOR','renderAllPrices','querySelector(\'h3\')']
for pat in patterns:
    print('\n###',pat)
    start=0
    hits=0
    while True:
        i=s.find(pat,start)
        if i<0 or hits>=4: break
        print('index',i)
        print(s[max(0,i-700):i+1800])
        start=i+1; hits+=1
