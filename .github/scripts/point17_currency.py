from pathlib import Path

p = Path("panel-privado.html")
s = p.read_text(encoding="utf-8")

css_anchor = """  input.stock-input[data-price-input], input.stock-input[data-price] { width: 64px; }\n"""
css_add = css_anchor + """  .currency-field { display:inline-flex; align-items:center; gap:6px; white-space:nowrap; }
  .currency-prefix { color:var(--ink-soft); font-size:11px; font-weight:700; letter-spacing:.02em; }
  .currency-field.compact-currency input.stock-input { width:78px; }
"""
assert css_anchor in s
s = s.replace(css_anchor, css_add, 1)

s = s.replace("function moneyFmt(n) { return '$' + Number(n).toFixed(2); }",
              "function moneyFmt(n) { return 'USD $' + Number(n).toFixed(2); }", 1)

s = s.replace(">$0.00<", ">USD $0.00<")
s = s.replace("<th>Precio</th>", "<th>Precio (USD)</th>")
s = s.replace('<label for="newProductPrice">Precio</label>', '<label for="newProductPrice">Precio (USD)</label>', 1)

old_new_price = '<input type="number" min="0" step="0.01" id="newProductPrice" placeholder="$" style="margin-bottom:0;">'
new_new_price = '<div class="currency-field"><span class="currency-prefix">USD $</span><input type="number" min="0" step="0.01" id="newProductPrice" placeholder="0.00" style="margin-bottom:0;"></div>'
assert old_new_price in s
s = s.replace(old_new_price, new_new_price, 1)

old_inventory = '<td><input type="number" min="0" step="0.01" class="stock-input" data-price-input value="${p.regular_price ?? \'\'}" placeholder="$"></td>'
new_inventory = '<td><div class="currency-field compact-currency"><span class="currency-prefix">USD $</span><input type="number" min="0" step="0.01" class="stock-input" data-price-input value="${p.regular_price ?? \'\'}" placeholder="0.00" aria-label="Precio en USD"></div></td>'
assert old_inventory in s
s = s.replace(old_inventory, new_inventory, 1)

old_upcoming = '<td><input type="number" min="0" step="0.01" class="stock-input" data-price value="${priceVal}" placeholder="$"></td>'
new_upcoming = '<td><div class="currency-field compact-currency"><span class="currency-prefix">USD $</span><input type="number" min="0" step="0.01" class="stock-input" data-price value="${priceVal}" placeholder="0.00" aria-label="Precio en USD"></div></td>'
assert old_upcoming in s
s = s.replace(old_upcoming, new_upcoming, 1)

s = s.replace(
    "const headers = ['Código', 'Estado', 'Forma de pago', 'Tipo', 'Total', 'Cobrado', 'Saldo pendiente', 'Fecha de creación', 'Fecha de reserva', 'Fecha de pago', 'Fecha de cancelación'];",
    "const headers = ['Código', 'Estado', 'Forma de pago', 'Tipo', 'Total (USD)', 'Cobrado (USD)', 'Saldo pendiente (USD)', 'Fecha de creación', 'Fecha de reserva', 'Fecha de pago', 'Fecha de cancelación'];",
    1
)

p.write_text(s, encoding="utf-8")
print("Point 17 USD patch applied")
