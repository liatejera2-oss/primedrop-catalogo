from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')
original = s

old_steps = '''      <ol class="purchase-steps">
        <li id="purchaseCopiedNote">Ya copiamos tu mensaje.</li>
        <li>Se va a abrir Instagram en una pestaña nueva.</li>
        <li>Toca el cuadro de mensaje y <strong>mantén presionado → Pegar</strong>.</li>
        <li>Envíalo — Prime Drop te confirma disponibilidad, pago y entrega ahí mismo.</li>
      </ol>
'''
new_steps = '''      <ol class="purchase-steps">
        <li id="purchaseCopiedNote">Tu mensaje está listo y ya lo copiamos.</li>
        <li>Abre <strong>@primedrop.pa</strong> en Instagram.</li>
        <li>Pega el mensaje en el chat y envíalo.</li>
        <li>Prime Drop te confirmará pago y entrega por Instagram.</li>
      </ol>
'''
if old_steps not in s:
    raise SystemExit('success steps anchor not found')
s = s.replace(old_steps, new_steps, 1)

old_link = '''      <a class="purchase-ig-link" id="purchaseIgLink" href="https://www.instagram.com/primedrop.pa/" target="_blank" rel="noopener noreferrer">Abrir Instagram ↗</a>'''
new_link = '''      <a class="purchase-ig-link" id="purchaseIgLink" href="https://www.instagram.com/primedrop.pa/" target="_blank" rel="noopener noreferrer">Abrir @primedrop.pa ↗</a>'''
if old_link not in s:
    raise SystemExit('instagram link anchor not found')
s = s.replace(old_link, new_link, 1)

old_message = '''      const paymentLine = row.payment_mode === 'deposit'
        ? `Forma de pago: Abono (50%) — pago ahora: ${moneyFmt(row.amount_due_now)} · saldo contra-entrega: ${moneyFmt(row.balance_due)}`
        : `Forma de pago: Pago completo — ${moneyFmt(row.amount_due_now)}`;

      const modalidadLine = row.fulfillment_type === 'backorder'
        ? 'Modalidad: Por pedido (no hay en inventario ahora, se pedirá especialmente)'
        : `Modalidad: ${row.sale_mode === 'preorder' ? 'Por encargo' : 'Disponible'}`;

      const message = 'Hola, Prime Drop. Creé una solicitud desde el catálogo.\\n\\n' +
        `Código: ${row.order_number}\\n` +
        `Producto: ${row.product_name}\\n` +
        (row.color ? `Color: ${row.color}\\n` : '') +
        `Talla: ${row.size}\\n` +
        `Cantidad: ${row.quantity}\\n` +
        `Precio unitario: ${moneyFmt(row.unit_price)}\\n` +
        `Total de referencia: ${moneyFmt(row.total_reference)}\\n` +
        `${modalidadLine}\\n` +
        `${paymentLine}\\n\\n` +
        '¿Me pueden confirmar disponibilidad, pago y entrega?';
'''
new_message = '''      const paymentLine = row.payment_mode === 'deposit'
        ? `Forma de pago: Abono (50%) · Pagas ahora: ${moneyFmt(row.amount_due_now)} · Saldo contra entrega: ${moneyFmt(row.balance_due)}`
        : 'Forma de pago: Pago completo';

      const availabilityLine = row.fulfillment_type === 'backorder'
        ? 'Disponibilidad: Por pedido'
        : `Disponibilidad: ${row.sale_mode === 'preorder' ? 'Por encargo' : 'En stock'}`;

      const unitPriceLine = Number(row.quantity) > 1
        ? `Precio unitario: ${moneyFmt(row.unit_price)}\\n`
        : '';

      const message = 'Hola, Prime Drop. Quiero comprar esta pieza del catálogo.\\n\\n' +
        `Solicitud: ${row.order_number}\\n` +
        `Producto: ${row.product_name}\\n` +
        (row.color ? `Color: ${row.color}\\n` : '') +
        `Talla: ${row.size}\\n` +
        `Cantidad: ${row.quantity}\\n` +
        unitPriceLine +
        `Total: ${moneyFmt(row.total_reference)}\\n` +
        `${availabilityLine}\\n` +
        `${paymentLine}\\n\\n` +
        '¿Me confirman los datos de pago y entrega para completar la compra?';
'''
if old_message not in s:
    raise SystemExit('message composition anchor not found')
s = s.replace(old_message, new_message, 1)

old_copied = '''      copiedNoteEl.textContent = copied
        ? 'Ya copiamos tu mensaje.'
        : 'No se pudo copiar automáticamente — selecciona el texto de abajo y cópialo a mano.';'''
new_copied = '''      copiedNoteEl.textContent = copied
        ? 'Tu mensaje está listo y ya lo copiamos.'
        : 'No se pudo copiar automáticamente — selecciona el mensaje de abajo y cópialo manualmente.';'''
if old_copied not in s:
    raise SystemExit('copied state anchor not found')
s = s.replace(old_copied, new_copied, 1)

required = [
    'Quiero comprar esta pieza del catálogo.',
    '`Solicitud: ${row.order_number}\\n`',
    '(row.color ? `Color: ${row.color}\\n` : \'\')',
    "'Disponibilidad: Por pedido'",
    "'Forma de pago: Pago completo'",
    'Abrir @primedrop.pa ↗',
    'Prime Drop te confirmará pago y entrega por Instagram.'
]
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit(f'Point 10 validation failed: {missing}')

if s == original:
    raise SystemExit('No changes produced')
path.write_text(s, encoding='utf-8')
