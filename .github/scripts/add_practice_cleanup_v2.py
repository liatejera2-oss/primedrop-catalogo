from pathlib import Path

p = Path('panel-privado.html')
s = p.read_text(encoding='utf-8')

css_anchor = "  .analysis-note { margin-top:12px; color:var(--ink-soft); font-size:11.5px; line-height:1.5; }\n"
css_add = css_anchor + "  .cleanup-details { margin:16px 0 0; border-top:1px solid var(--panel-line); padding-top:14px; }\n  .cleanup-details summary { list-style:none; cursor:pointer; color:var(--ink-soft); font-size:12px; font-weight:700; width:max-content; }\n  .cleanup-details summary::-webkit-details-marker { display:none; }\n  .cleanup-details summary::after { content:' +'; }\n  .cleanup-details[open] summary::after { content:' −'; }\n  .cleanup-box { margin-top:12px; padding:14px; border:1px solid #ECD2D4; border-radius:12px; background:#FFF9F9; }\n  .cleanup-box p { color:var(--ink-soft); font-size:12px; line-height:1.5; margin:0 0 10px; max-width:760px; }\n  button.action-delete { background:transparent; color:#9A4B50; border-color:transparent; padding:5px 7px; min-height:30px; }\n  button.action-delete:hover { background:var(--danger-bg); color:var(--accent); }\n"
assert css_anchor in s, 'css anchor missing'
s = s.replace(css_anchor, css_add, 1)

html_anchor = '''        <div class="table-scroll orders-scroll">
          <table>
            <thead>
              <tr><th>Código</th><th>Total</th><th>Cobrado / por cobrar</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>
            </thead>
            <tbody id="ordersBody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <div id="viewInventario"'''
html_repl = '''        <div class="table-scroll orders-scroll">
          <table>
            <thead>
              <tr><th>Código</th><th>Total</th><th>Cobrado / por cobrar</th><th>Pago</th><th>Tipo</th><th>Creada</th><th>Estado</th><th>Acciones</th></tr>
            </thead>
            <tbody id="ordersBody"></tbody>
          </table>
        </div>
        <details class="cleanup-details">
          <summary>Datos de prueba</summary>
          <div class="cleanup-box">
            <p><strong>Reiniciar solicitudes</strong> elimina el historial de solicitudes y reinicia la numeración a PD-AAAA-0001. El inventario, productos, precios, tallas y colores permanecen exactamente como están.</p>
            <button class="danger-ghost" id="resetPracticeDataBtn">Reiniciar datos de prueba</button>
            <div id="resetPracticeMsg" style="margin-top:10px;"></div>
          </div>
        </details>
      </div>
    </div>

    <div id="viewInventario"'''
assert html_anchor in s, 'html anchor missing'
s = s.replace(html_anchor, html_repl, 1)

old_order_actions = '''    if (o.status === 'pending') {
      const confirmLabel = o.payment_mode === 'deposit' ? 'Confirmar abono' : 'Confirmar pago';
      actions = `<button class="action-confirm" data-action="pay" data-id="${o.id}" data-status="${o.status}" data-payment-mode="${o.payment_mode}">${confirmLabel}</button>
                 <button class="danger" data-action="cancel" data-id="${o.id}" data-status="${o.status}">Cancelar</button>`;
    } else if (o.status === 'reserved') {
      actions = `<button class="action-confirm" data-action="pay" data-id="${o.id}" data-status="${o.status}" data-payment-mode="${o.payment_mode}">Confirmar saldo</button>
                 <button class="danger" data-action="cancel" data-id="${o.id}" data-status="${o.status}">Cancelar reserva</button>`;
    }
'''
new_order_actions = '''    if (o.status === 'pending') {
      const confirmLabel = o.payment_mode === 'deposit' ? 'Confirmar abono' : 'Confirmar pago';
      actions = `<button class="action-confirm" data-action="pay" data-id="${o.id}" data-code="${o.order_number}" data-status="${o.status}" data-payment-mode="${o.payment_mode}">${confirmLabel}</button>
                 <button class="danger" data-action="cancel" data-id="${o.id}" data-code="${o.order_number}" data-status="${o.status}">Cancelar</button>`;
    } else if (o.status === 'reserved') {
      actions = `<button class="action-confirm" data-action="pay" data-id="${o.id}" data-code="${o.order_number}" data-status="${o.status}" data-payment-mode="${o.payment_mode}">Confirmar saldo</button>
                 <button class="danger" data-action="cancel" data-id="${o.id}" data-code="${o.order_number}" data-status="${o.status}">Cancelar reserva</button>`;
    }
    actions += `<button class="action-delete" data-action="delete" data-id="${o.id}" data-code="${o.order_number}" data-status="${o.status}" title="Borra solo el registro; no modifica inventario">Borrar</button>`;
'''
assert old_order_actions in s, 'order actions anchor missing'
s = s.replace(old_order_actions, new_order_actions, 1)

old_body_handler = '''    const currentStatus = btn.dataset.status;
    if (action === 'cancel') {
      const warning = currentStatus === 'reserved'
        ? 'Esta reserva ya tiene un abono confirmado. Al cancelarla se liberará el stock, pero cualquier devolución de dinero debe gestionarse manualmente. ¿Continuar?'
        : '¿Cancelar esta solicitud?';
      if (!confirm(warning)) return;
    }
    btn.disabled = true;

    const rpcName = action === 'pay' ? 'confirm_order_payment' : 'cancel_order';
    const { data, error } = await client.rpc(rpcName, { p_order_id: id });

    btn.disabled = false;
    if (error) { showMsg(ordersMsg, error.message, 'error'); return; }
    const row = Array.isArray(data) ? data[0] : data;
    const resultLabel = row.status === 'reserved'
      ? 'abono confirmado; pieza reservada y stock apartado'
      : row.status === 'paid'
        ? 'pago completado'
        : 'cancelada';
    showMsg(ordersMsg, `Solicitud ${row.order_number}: ${resultLabel}.`, 'ok');
    loadOrders(activeStatus);
    loadFinancialSummary();
    loadInventory();
'''
new_body_handler = '''    const currentStatus = btn.dataset.status;
    if (action === 'delete') {
      const code = btn.dataset.code || 'esta solicitud';
      if (!confirm(`¿Borrar ${code} del historial?\n\nEsto elimina el registro y sus datos de análisis, pero NO modifica el inventario. No se puede deshacer.`)) return;
      btn.disabled = true;
      const { error } = await client.rpc('delete_order_record_no_stock', { p_order_id: id });
      btn.disabled = false;
      if (error) { showMsg(ordersMsg, error.message, 'error'); return; }
      showMsg(ordersMsg, `${code} eliminado del historial. El inventario no cambió.`, 'ok');
      loadOrders(activeStatus);
      loadFinancialSummary();
      if (viewLoaded.analisis) loadAnalysis();
      return;
    }
    if (action === 'cancel') {
      const warning = currentStatus === 'reserved'
        ? 'Esta reserva ya tiene un abono confirmado. Al cancelarla se liberará el stock, pero cualquier devolución de dinero debe gestionarse manualmente. ¿Continuar?'
        : '¿Cancelar esta solicitud?';
      if (!confirm(warning)) return;
    }
    btn.disabled = true;

    const rpcName = action === 'pay' ? 'confirm_order_payment' : 'cancel_order';
    const { data, error } = await client.rpc(rpcName, { p_order_id: id });

    btn.disabled = false;
    if (error) { showMsg(ordersMsg, error.message, 'error'); return; }
    const row = Array.isArray(data) ? data[0] : data;
    const resultLabel = row.status === 'reserved'
      ? 'abono confirmado; pieza reservada y stock apartado'
      : row.status === 'paid'
        ? 'pago completado'
        : 'cancelada';
    showMsg(ordersMsg, `Solicitud ${row.order_number}: ${resultLabel}.`, 'ok');
    loadOrders(activeStatus);
    loadFinancialSummary();
    loadInventory();
    if (viewLoaded.analisis) loadAnalysis();
'''
assert old_body_handler in s, 'body handler anchor missing'
s = s.replace(old_body_handler, new_body_handler, 1)

old_search_actions = '''    if (order.status === 'pending') {
      const confirmLabel = order.payment_mode === 'deposit' ? 'Confirmar abono' : 'Confirmar pago';
      actions = `<div class="row" style="margin-top:10px;">
        <button class="action-confirm" data-action="pay" data-id="${order.id}" data-status="${order.status}">${confirmLabel}</button>
        <button class="danger" data-action="cancel" data-id="${order.id}" data-status="${order.status}">Cancelar</button>
      </div>`;
    } else if (order.status === 'reserved') {
      actions = `<div class="row" style="margin-top:10px;">
        <button class="action-confirm" data-action="pay" data-id="${order.id}" data-status="${order.status}">Confirmar saldo</button>
        <button class="danger" data-action="cancel" data-id="${order.id}" data-status="${order.status}">Cancelar reserva</button>
      </div>`;
    }
'''
new_search_actions = '''    if (order.status === 'pending') {
      const confirmLabel = order.payment_mode === 'deposit' ? 'Confirmar abono' : 'Confirmar pago';
      actions = `<div class="row" style="margin-top:10px;">
        <button class="action-confirm" data-action="pay" data-id="${order.id}" data-code="${order.order_number}" data-status="${order.status}">${confirmLabel}</button>
        <button class="danger" data-action="cancel" data-id="${order.id}" data-code="${order.order_number}" data-status="${order.status}">Cancelar</button>
        <button class="action-delete" data-action="delete" data-id="${order.id}" data-code="${order.order_number}" data-status="${order.status}">Borrar</button>
      </div>`;
    } else if (order.status === 'reserved') {
      actions = `<div class="row" style="margin-top:10px;">
        <button class="action-confirm" data-action="pay" data-id="${order.id}" data-code="${order.order_number}" data-status="${order.status}">Confirmar saldo</button>
        <button class="danger" data-action="cancel" data-id="${order.id}" data-code="${order.order_number}" data-status="${order.status}">Cancelar reserva</button>
        <button class="action-delete" data-action="delete" data-id="${order.id}" data-code="${order.order_number}" data-status="${order.status}">Borrar</button>
      </div>`;
    } else {
      actions = `<div class="row" style="margin-top:10px;"><button class="action-delete" data-action="delete" data-id="${order.id}" data-code="${order.order_number}" data-status="${order.status}">Borrar</button></div>`;
    }
'''
assert old_search_actions in s, 'search actions anchor missing'
s = s.replace(old_search_actions, new_search_actions, 1)

old_search_handler = '''        if (btn.dataset.action === 'cancel') {
          const warning = btn.dataset.status === 'reserved'
            ? 'Esta reserva tiene un abono confirmado. Se liberará el stock y cualquier devolución de dinero se gestiona manualmente. ¿Continuar?'
            : '¿Cancelar esta solicitud?';
          if (!confirm(warning)) return;
        }
        const rpcName = btn.dataset.action === 'pay' ? 'confirm_order_payment' : 'cancel_order';
        const { data, error } = await client.rpc(rpcName, { p_order_id: btn.dataset.id });
        if (error) { resultEl.innerHTML += `<p class="msg msg-error">${error.message}</p>`; return; }
        document.getElementById('searchBtn').click();
        loadOrders(activeStatus);
        loadInventory();
'''
new_search_handler = '''        if (btn.dataset.action === 'delete') {
          const code = btn.dataset.code || order.order_number;
          if (!confirm(`¿Borrar ${code} del historial?\n\nEl inventario no se modificará.`)) return;
          const { error } = await client.rpc('delete_order_record_no_stock', { p_order_id: btn.dataset.id });
          if (error) { resultEl.innerHTML += `<p class="msg msg-error">${error.message}</p>`; return; }
          resultEl.innerHTML = '<p class="msg msg-ok">Solicitud eliminada. El inventario no cambió.</p>';
          loadOrders(activeStatus);
          loadFinancialSummary();
          if (viewLoaded.analisis) loadAnalysis();
          return;
        }
        if (btn.dataset.action === 'cancel') {
          const warning = btn.dataset.status === 'reserved'
            ? 'Esta reserva tiene un abono confirmado. Se liberará el stock y cualquier devolución de dinero se gestiona manualmente. ¿Continuar?'
            : '¿Cancelar esta solicitud?';
          if (!confirm(warning)) return;
        }
        const rpcName = btn.dataset.action === 'pay' ? 'confirm_order_payment' : 'cancel_order';
        const { data, error } = await client.rpc(rpcName, { p_order_id: btn.dataset.id });
        if (error) { resultEl.innerHTML += `<p class="msg msg-error">${error.message}</p>`; return; }
        document.getElementById('searchBtn').click();
        loadOrders(activeStatus);
        loadFinancialSummary();
        loadInventory();
        if (viewLoaded.analisis) loadAnalysis();
'''
assert old_search_handler in s, 'search handler anchor missing'
s = s.replace(old_search_handler, new_search_handler, 1)

reset_anchor = "  document.getElementById('analysisWindow').addEventListener('change', loadAnalysis);\n\n  // ---- Inventario ----\n"
reset_code = '''  document.getElementById('analysisWindow').addEventListener('change', loadAnalysis);

  const resetPracticeDataBtn = document.getElementById('resetPracticeDataBtn');
  if (resetPracticeDataBtn) {
    resetPracticeDataBtn.addEventListener('click', async () => {
      const msgEl = document.getElementById('resetPracticeMsg');
      const ok = confirm('Esto borrará TODAS las solicitudes de prueba y reiniciará la numeración.\n\nEl inventario, productos, precios, tallas y colores NO se modificarán. ¿Continuar?');
      if (!ok) return;
      const typed = prompt('Para confirmar, escribe BORRAR');
      if (typed !== 'BORRAR') {
        showMsg(msgEl, 'No se realizó ningún cambio.', 'error');
        return;
      }
      resetPracticeDataBtn.disabled = true;
      const { data, error } = await client.rpc('reset_practice_orders_no_stock');
      resetPracticeDataBtn.disabled = false;
      if (error) { showMsg(msgEl, error.message, 'error'); return; }
      const row = Array.isArray(data) ? data[0] : data;
      showMsg(msgEl, `${row?.deleted_orders ?? 0} solicitudes eliminadas. La próxima solicitud será ${row?.next_order_number || 'PD-AAAA-0001'}. El inventario quedó intacto.`, 'ok');
      document.getElementById('searchResult').innerHTML = '';
      loadOrders(activeStatus);
      loadFinancialSummary();
      if (viewLoaded.analisis) loadAnalysis();
    });
  }

  // ---- Inventario ----
'''
assert reset_anchor in s, 'reset anchor missing'
s = s.replace(reset_anchor, reset_code, 1)

p.write_text(s, encoding='utf-8')
print('patched practice cleanup controls')
