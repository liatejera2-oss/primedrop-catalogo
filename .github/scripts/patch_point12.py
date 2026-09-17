from pathlib import Path

path = Path('panel-privado.html')
s = path.read_text(encoding='utf-8')
original = s

# 1) Internal reservation visual state.
anchor = "  .badge-pending { background: #FFF3D6; color: #8A6300; }\n  .badge-paid { background: #DFF3E3; color: #1E7A34; }"
replacement = "  .badge-pending { background: #FFF3D6; color: #8A6300; }\n  .badge-reserved { background: #EEE9FF; color: #5A3BA4; }\n  .badge-paid { background: #DFF3E3; color: #1E7A34; }"
if anchor not in s: raise SystemExit('CSS badge anchor not found')
s = s.replace(anchor, replacement, 1)

# 2) Internal policy note and new Reserved tab.
anchor = '''      <div class="card">\n        <h2>Solicitudes</h2>\n        <div class="tabs">\n          <button class="tab-btn active" data-status="pending">Pendientes</button>\n          <button class="tab-btn" data-status="paid">Pagadas</button>\n          <button class="tab-btn" data-status="cancelled">Canceladas</button>\n        </div>'''
replacement = '''      <div class="card">\n        <h2>Solicitudes</h2>\n        <p class="sub" style="margin-bottom:14px;"><strong>Regla interna de reserva:</strong> una solicitud con abono no aparta stock hasta que confirmes el 50%. Al confirmar el abono pasa a <strong>Reservadas</strong> y el inventario se descuenta una sola vez. Al cobrar el saldo pasa a Pagadas sin volver a descontar. Si cancelas una reserva, el stock se libera; cualquier devolución de dinero se gestiona manualmente. Las reservas con abono confirmado no vencen automáticamente.</p>\n        <div class="tabs">\n          <button class="tab-btn active" data-status="pending">Pendientes</button>\n          <button class="tab-btn" data-status="reserved">Reservadas</button>\n          <button class="tab-btn" data-status="paid">Pagadas</button>\n          <button class="tab-btn" data-status="cancelled">Canceladas</button>\n        </div>'''
if anchor not in s: raise SystemExit('Solicitudes tabs anchor not found')
s = s.replace(anchor, replacement, 1)

# 3) Show money movement directly in the table.
anchor = '<tr><th>Código</th><th>Total</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>'
replacement = '<tr><th>Código</th><th>Total</th><th>Cobrado / saldo</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>'
if anchor not in s: raise SystemExit('Orders header anchor not found')
s = s.replace(anchor, replacement, 1)

# 4) Reservation badge and internal money helper.
anchor = '''  function badgeFor(status) {\n    const label = status === 'pending' ? 'Pendiente' : status === 'paid' ? 'Pagada' : 'Cancelada';\n    return `<span class="badge badge-${status}">${label}</span>`;\n  }'''
replacement = '''  function badgeFor(status) {\n    const labels = { pending: 'Pendiente', reserved: 'Reservada', paid: 'Pagada', cancelled: 'Cancelada' };\n    return `<span class="badge badge-${status}">${labels[status] || status}</span>`;\n  }\n\n  function paymentProgressHtml(order) {\n    const total = Number(order.total_reference || 0);\n    const paid = Number(order.amount_paid || 0);\n    const balance = Math.max(0, total - paid);\n    return `<span>${moneyFmt(paid)} cobrado</span><br><span style="color:var(--ink-soft);">${moneyFmt(balance)} saldo</span>`;\n  }'''
if anchor not in s: raise SystemExit('badgeFor anchor not found')
s = s.replace(anchor, replacement, 1)

# 5) Load the new internal payment fields.
anchor = ".select('id, order_number, status, total_reference, payment_mode, fulfillment_type, created_at')"
replacement = ".select('id, order_number, status, total_reference, amount_paid, payment_mode, fulfillment_type, created_at, reserved_at, paid_at')"
if anchor not in s: raise SystemExit('loadOrders select anchor not found')
s = s.replace(anchor, replacement, 1)

anchor = "if (!data.length) { tbody.innerHTML = '<tr><td colspan=\"5\" style=\"color:var(--ink-soft);\">Sin solicitudes en este estado.</td></tr>'; return; }"
replacement = "if (!data.length) { tbody.innerHTML = '<tr><td colspan=\"8\" style=\"color:var(--ink-soft);\">Sin solicitudes en este estado.</td></tr>'; return; }"
if anchor not in s: raise SystemExit('empty orders colspan anchor not found')
s = s.replace(anchor, replacement, 1)

# 6) Order actions: pending deposit -> reserve; reserved -> complete balance.
anchor = '''    let actions = '';\n    if (o.status === 'pending') {\n      actions = `<button data-action="pay" data-id="${o.id}">Marcar pagada</button>\n                 <button class="danger" data-action="cancel" data-id="${o.id}">Cancelar</button>`;\n    }\n    tr.innerHTML = `\n      <td>${o.order_number}</td>\n      <td>${moneyFmt(o.total_reference)}</td>\n      <td>${paymentBadgeFor(o.payment_mode)}</td>\n      <td>${fulfillmentBadgeFor(o.fulfillment_type)}</td>\n      <td>${created}</td>\n      <td>${badgeFor(o.status)}</td>\n      <td>${actions}</td>\n    `;'''
replacement = '''    let actions = '';\n    if (o.status === 'pending') {\n      const confirmLabel = o.payment_mode === 'deposit' ? 'Confirmar abono 50%' : 'Confirmar pago';\n      actions = `<button data-action="pay" data-id="${o.id}" data-status="${o.status}" data-payment-mode="${o.payment_mode}">${confirmLabel}</button>\n                 <button class="danger" data-action="cancel" data-id="${o.id}" data-status="${o.status}">Cancelar</button>`;\n    } else if (o.status === 'reserved') {\n      actions = `<button data-action="pay" data-id="${o.id}" data-status="${o.status}" data-payment-mode="${o.payment_mode}">Completar pago</button>\n                 <button class="danger" data-action="cancel" data-id="${o.id}" data-status="${o.status}">Cancelar / liberar stock</button>`;\n    }\n    tr.innerHTML = `\n      <td>${o.order_number}</td>\n      <td>${moneyFmt(o.total_reference)}</td>\n      <td>${paymentProgressHtml(o)}</td>\n      <td>${paymentBadgeFor(o.payment_mode)}</td>\n      <td>${fulfillmentBadgeFor(o.fulfillment_type)}</td>\n      <td>${created}</td>\n      <td>${badgeFor(o.status)}</td>\n      <td>${actions}</td>\n    `;'''
if anchor not in s: raise SystemExit('orderRow anchor not found')
s = s.replace(anchor, replacement, 1)

# 7) Main list action handler: confirm risky transitions and report reserved separately.
anchor = '''    const ordersMsg = document.getElementById('ordersMsg');\n    btn.disabled = true;\n\n    const rpcName = action === 'pay' ? 'confirm_order_payment' : 'cancel_order';\n    const { data, error } = await client.rpc(rpcName, { p_order_id: id });\n\n    btn.disabled = false;\n    if (error) { showMsg(ordersMsg, error.message, 'error'); return; }\n    const row = Array.isArray(data) ? data[0] : data;\n    showMsg(ordersMsg, `Solicitud ${row.order_number}: ${row.status === 'paid' ? 'marcada como pagada' : 'cancelada'}.`, 'ok');'''
replacement = '''    const ordersMsg = document.getElementById('ordersMsg');\n    const currentStatus = btn.dataset.status;\n    if (action === 'cancel') {\n      const warning = currentStatus === 'reserved'\n        ? 'Esta reserva ya tiene un abono confirmado. Al cancelarla se liberará el stock, pero cualquier devolución de dinero debe gestionarse manualmente. ¿Continuar?'\n        : '¿Cancelar esta solicitud?';\n      if (!confirm(warning)) return;\n    }\n    btn.disabled = true;\n\n    const rpcName = action === 'pay' ? 'confirm_order_payment' : 'cancel_order';\n    const { data, error } = await client.rpc(rpcName, { p_order_id: id });\n\n    btn.disabled = false;\n    if (error) { showMsg(ordersMsg, error.message, 'error'); return; }\n    const row = Array.isArray(data) ? data[0] : data;\n    const resultLabel = row.status === 'reserved'\n      ? 'abono confirmado; pieza reservada y stock apartado'\n      : row.status === 'paid'\n        ? 'pago completado'\n        : 'cancelada';\n    showMsg(ordersMsg, `Solicitud ${row.order_number}: ${resultLabel}.`, 'ok');'''
if anchor not in s: raise SystemExit('orders action handler anchor not found')
s = s.replace(anchor, replacement, 1)

# 8) Search view includes reservation/payment accounting.
anchor = ".select('id, order_number, status, total_reference, payment_mode, fulfillment_type, created_at, paid_at, cancelled_at')"
replacement = ".select('id, order_number, status, total_reference, amount_paid, payment_mode, fulfillment_type, created_at, reserved_at, paid_at, cancelled_at')"
if anchor not in s: raise SystemExit('search select anchor not found')
s = s.replace(anchor, replacement, 1)

anchor = '''    let actions = '';\n    if (order.status === 'pending') {\n      actions = `<div class="row" style="margin-top:10px;">\n        <button data-action="pay" data-id="${order.id}">Marcar pagada</button>\n        <button class="danger" data-action="cancel" data-id="${order.id}">Cancelar</button>\n      </div>`;\n    }'''
replacement = '''    let actions = '';\n    if (order.status === 'pending') {\n      const confirmLabel = order.payment_mode === 'deposit' ? 'Confirmar abono 50%' : 'Confirmar pago';\n      actions = `<div class="row" style="margin-top:10px;">\n        <button data-action="pay" data-id="${order.id}" data-status="${order.status}">${confirmLabel}</button>\n        <button class="danger" data-action="cancel" data-id="${order.id}" data-status="${order.status}">Cancelar</button>\n      </div>`;\n    } else if (order.status === 'reserved') {\n      actions = `<div class="row" style="margin-top:10px;">\n        <button data-action="pay" data-id="${order.id}" data-status="${order.status}">Completar pago</button>\n        <button class="danger" data-action="cancel" data-id="${order.id}" data-status="${order.status}">Cancelar / liberar stock</button>\n      </div>`;\n    }'''
if anchor not in s: raise SystemExit('search actions anchor not found')
s = s.replace(anchor, replacement, 1)

anchor = '''      <p style="margin:6px 0;">${itemsHtml}</p>\n      <p>Total de referencia: ${moneyFmt(order.total_reference)}</p>\n      ${actions}'''
replacement = '''      <p style="margin:6px 0;">${itemsHtml}</p>\n      <p>Total: ${moneyFmt(order.total_reference)} · Cobrado: ${moneyFmt(order.amount_paid || 0)} · Saldo: ${moneyFmt(Math.max(0, Number(order.total_reference) - Number(order.amount_paid || 0)))}</p>\n      ${order.reserved_at ? `<p style="margin-top:4px;color:var(--ink-soft);">Reserva confirmada: ${new Date(order.reserved_at).toLocaleString('es-PA')}</p>` : ''}\n      ${actions}'''
if anchor not in s: raise SystemExit('search summary anchor not found')
s = s.replace(anchor, replacement, 1)

# 9) Search action cancellation warning.
anchor = '''        if (!btn) return;\n        const rpcName = btn.dataset.action === 'pay' ? 'confirm_order_payment' : 'cancel_order';\n        const { data, error } = await client.rpc(rpcName, { p_order_id: btn.dataset.id });'''
replacement = '''        if (!btn) return;\n        if (btn.dataset.action === 'cancel') {\n          const warning = btn.dataset.status === 'reserved'\n            ? 'Esta reserva tiene un abono confirmado. Se liberará el stock y cualquier devolución de dinero se gestiona manualmente. ¿Continuar?'\n            : '¿Cancelar esta solicitud?';\n          if (!confirm(warning)) return;\n        }\n        const rpcName = btn.dataset.action === 'pay' ? 'confirm_order_payment' : 'cancel_order';\n        const { data, error } = await client.rpc(rpcName, { p_order_id: btn.dataset.id });'''
if anchor not in s: raise SystemExit('search action handler anchor not found')
s = s.replace(anchor, replacement, 1)

# 10) CSV becomes a real internal reconciliation export.
anchor = ".select('order_number, status, total_reference, payment_mode, fulfillment_type, created_at, paid_at')"
replacement = ".select('order_number, status, total_reference, amount_paid, payment_mode, fulfillment_type, created_at, reserved_at, paid_at, cancelled_at')"
if anchor not in s: raise SystemExit('CSV select anchor not found')
s = s.replace(anchor, replacement, 1)

anchor = "const statusLabel = { pending: 'Pendiente', paid: 'Pagada', cancelled: 'Cancelada' };"
replacement = "const statusLabel = { pending: 'Pendiente', reserved: 'Reservada', paid: 'Pagada', cancelled: 'Cancelada' };"
if anchor not in s: raise SystemExit('CSV status labels anchor not found')
s = s.replace(anchor, replacement, 1)

anchor = "const headers = ['Código', 'Estado', 'Forma de pago', 'Tipo', 'Total de la prenda', 'Monto a cobrar', 'Fecha de creación', 'Fecha de pago'];"
replacement = "const headers = ['Código', 'Estado', 'Forma de pago', 'Tipo', 'Total', 'Cobrado', 'Saldo pendiente', 'Fecha de creación', 'Fecha de reserva', 'Fecha de pago', 'Fecha de cancelación'];"
if anchor not in s: raise SystemExit('CSV headers anchor not found')
s = s.replace(anchor, replacement, 1)

anchor = '''      const total = Number(o.total_reference);\n      const amountDue = o.payment_mode === 'deposit' ? Math.round(total * DEPOSIT_RATIO * 100) / 100 : total;\n      return [\n        o.order_number,\n        statusLabel[o.status] || o.status,\n        paymentLabel[o.payment_mode] || o.payment_mode,\n        fulfillmentLabel[o.fulfillment_type] || o.fulfillment_type,\n        total.toFixed(2),\n        amountDue.toFixed(2),\n        new Date(o.created_at).toLocaleString('es-PA'),\n        o.paid_at ? new Date(o.paid_at).toLocaleString('es-PA') : ''\n      ];'''
replacement = '''      const total = Number(o.total_reference);\n      const paid = Number(o.amount_paid || 0);\n      const balance = Math.max(0, total - paid);\n      return [\n        o.order_number,\n        statusLabel[o.status] || o.status,\n        paymentLabel[o.payment_mode] || o.payment_mode,\n        fulfillmentLabel[o.fulfillment_type] || o.fulfillment_type,\n        total.toFixed(2),\n        paid.toFixed(2),\n        balance.toFixed(2),\n        new Date(o.created_at).toLocaleString('es-PA'),\n        o.reserved_at ? new Date(o.reserved_at).toLocaleString('es-PA') : '',\n        o.paid_at ? new Date(o.paid_at).toLocaleString('es-PA') : '',\n        o.cancelled_at ? new Date(o.cancelled_at).toLocaleString('es-PA') : ''\n      ];'''
if anchor not in s: raise SystemExit('CSV rows anchor not found')
s = s.replace(anchor, replacement, 1)

required = [
    'data-status="reserved">Reservadas',
    'Confirmar abono 50%',
    'Completar pago',
    'Cancelar / liberar stock',
    'paymentProgressHtml',
    "reserved: 'Reservada'",
    'Las reservas con abono confirmado no vencen automáticamente.',
    "amount_paid, payment_mode",
    "'Fecha de reserva'",
]
missing = [x for x in required if x not in s]
if missing: raise SystemExit(f'Point 12 validation failed: {missing}')
if s == original: raise SystemExit('No Point 12 changes produced')
path.write_text(s, encoding='utf-8')
