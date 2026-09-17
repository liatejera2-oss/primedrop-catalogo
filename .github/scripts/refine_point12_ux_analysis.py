from pathlib import Path
import re

p = Path('panel-privado.html')
s = p.read_text(encoding='utf-8')

def replace_once(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'anchor not found: {label}')
    s = s.replace(old, new, 1)

# 1) Semantic UI system + cleaner financial summary + analysis UI.
style = r'''
<style id="point12-ux-finance-analysis">
  :root {
    --success:#2F6B4F; --success-bg:#EEF6F1; --success-line:#CFE2D7;
    --warning:#8A6300; --warning-bg:#FFF7E3; --warning-line:#EBD9A5;
    --danger-bg:#FFF2F2; --neutral-fill:#F2F3F2; --neutral-bar:#66707A;
  }
  button { background:transparent; color:var(--ink); border:1px solid var(--panel-line); }
  button:hover { background:#F2F2F0; }
  button:disabled { background:#F1F1EF; color:var(--ink-soft); border-color:var(--panel-line); opacity:.72; }
  #loginBtn, .publish-btn { background:var(--ink); color:#fff; border-color:var(--ink); }
  #loginBtn:hover, .publish-btn:hover { background:#111; }
  button.action-confirm { background:var(--success-bg); color:var(--success); border-color:var(--success-line); }
  button.action-confirm:hover { background:#E3F0E8; }
  button.danger, button.danger-ghost { background:transparent; color:var(--accent); border-color:#E8B8BC; }
  button.danger:hover, button.danger-ghost:hover { background:var(--danger-bg); }
  .tab-btn.active { background:#E9EAE8; color:var(--ink); border-color:#E9EAE8; }
  .badge-full, .badge-deposit { background:#F1F2F2; color:#5E6268; }
  .badge-stock { background:#F1F2F2; color:var(--ink-soft); }
  .badge-backorder { background:var(--warning-bg); color:var(--warning); }

  .finance-summary { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:20px; }
  .finance-block { background:#fff; border:1px solid var(--panel-line); border-radius:16px; padding:18px; }
  .finance-kicker { color:var(--ink-soft); font-size:10.5px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; margin-bottom:10px; }
  .finance-primary { display:flex; align-items:end; justify-content:space-between; gap:16px; padding-bottom:14px; border-bottom:1px solid var(--panel-line); }
  .finance-primary span { color:var(--ink-soft); font-size:12px; font-weight:650; }
  .finance-primary strong { font-size:26px; letter-spacing:-.035em; font-weight:700; }
  .finance-split { display:grid; grid-template-columns:1fr 1fr; gap:16px; padding-top:14px; }
  .finance-metric span { display:block; color:var(--ink-soft); font-size:11.5px; margin-bottom:4px; }
  .finance-metric strong { display:block; font-size:17px; letter-spacing:-.02em; }
  .finance-metric small { display:block; margin-top:3px; color:var(--ink-soft); font-size:11px; line-height:1.35; }
  .finance-block-pending .finance-split { padding-top:0; }
  .finance-block-pending .finance-metric { padding:12px 0; }
  .finance-block-pending .finance-metric + .finance-metric { border-left:1px solid var(--panel-line); padding-left:16px; }
  .finance-note { grid-column:1/-1; color:var(--ink-soft); font-size:11.5px; padding:0 2px; line-height:1.45; }

  .analysis-header { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin-bottom:18px; }
  .analysis-header .section-intro { margin-bottom:0; }
  .analysis-period { min-width:150px; }
  .analysis-period label { margin-bottom:5px; }
  .analysis-period select { width:100%; }
  .analysis-summary-line { display:flex; gap:18px; flex-wrap:wrap; padding:12px 14px; margin-bottom:18px; border:1px solid var(--panel-line); border-radius:12px; background:#FAFAF8; }
  .analysis-summary-line span { color:var(--ink-soft); font-size:12px; }
  .analysis-summary-line strong { color:var(--ink); font-size:13px; }
  .demand-chart { border:1px solid var(--panel-line); border-radius:14px; padding:16px; background:#fff; margin-bottom:18px; }
  .demand-chart h3 { font-size:13.5px; margin-bottom:14px; }
  .demand-row { display:grid; grid-template-columns:minmax(150px,240px) minmax(160px,1fr) auto; align-items:center; gap:12px; padding:8px 0; }
  .demand-name { min-width:0; font-size:12.5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .demand-track { height:8px; border-radius:999px; background:#ECEDEA; overflow:hidden; }
  .demand-fill { height:100%; border-radius:999px; background:var(--neutral-bar); }
  .demand-meta { min-width:118px; text-align:right; color:var(--ink-soft); font-size:11px; }
  .analysis-scroll table { min-width:860px; width:100%; }
  .signal { display:inline-flex; align-items:center; border-radius:999px; padding:4px 8px; font-size:11px; font-weight:700; border:1px solid var(--panel-line); background:#F6F6F4; color:var(--ink-soft); }
  .signal-critical { color:var(--accent); background:var(--danger-bg); border-color:#E8B8BC; }
  .signal-watch { color:var(--warning); background:var(--warning-bg); border-color:var(--warning-line); }
  .signal-ok { color:var(--success); background:var(--success-bg); border-color:var(--success-line); }
  .analysis-note { margin-top:12px; color:var(--ink-soft); font-size:11.5px; line-height:1.5; }

  @media (max-width:900px) {
    .finance-summary { grid-template-columns:1fr; }
    .analysis-header { flex-direction:column; }
    .analysis-period { width:100%; }
  }
  @media (max-width:760px) {
    .finance-primary { align-items:flex-start; flex-direction:column; gap:5px; }
    .finance-split { grid-template-columns:1fr; gap:10px; }
    .finance-block-pending .finance-metric + .finance-metric { border-left:0; border-top:1px solid var(--panel-line); padding-left:0; }
    .demand-row { grid-template-columns:1fr; gap:5px; }
    .demand-meta { text-align:left; }
  }
</style>
'''
replace_once('</head>', style + '\n</head>', 'head style insertion')

# 2) Navigation.
replace_once(
'      <button class="view-tab-btn" data-view="gastos">Gastos Operativos</button>\n',
'      <button class="view-tab-btn" data-view="gastos">Gastos Operativos</button>\n      <button class="view-tab-btn" data-view="analisis">Análisis</button>\n',
'analysis nav tab')

# 3) Financial summary: two conceptual groups, only one legitimate combined amount.
old_finance = '''      <div class="finance-summary" id="financialSummary" aria-label="Resumen financiero básico">
        <div class="finance-card"><span>Cobrado confirmado</span><strong id="summaryCollected">$0.00</strong><small>Abonos y pagos confirmados.</small></div>
        <div class="finance-card"><span>Por cobrar</span><strong id="summaryReceivable">$0.00</strong><small>Solicitudes pendientes + saldo de reservas.</small></div>
        <div class="finance-card"><span>En reservas</span><strong id="summaryReserved">$0.00</strong><small id="summaryReservedCount">0 reservas activas.</small></div>
        <div class="finance-card"><span>Ventas completadas</span><strong id="summaryPaidSales">$0.00</strong><small id="summaryPaidCount">0 ventas pagadas.</small></div>
        <div class="finance-note">Resumen operativo básico. No incluye solicitudes canceladas, devoluciones ni gastos.</div>
      </div>
'''
new_finance = '''      <div class="finance-summary" id="financialSummary" aria-label="Resumen financiero básico">
        <section class="finance-block">
          <div class="finance-kicker">Caja</div>
          <div class="finance-primary"><span>Caja recibida</span><strong id="summaryCollected">$0.00</strong></div>
          <div class="finance-split">
            <div class="finance-metric"><span>Ventas pagadas</span><strong id="summaryPaidSales">$0.00</strong><small id="summaryPaidCount">0 ventas pagadas.</small></div>
            <div class="finance-metric"><span>Abonos vigentes</span><strong id="summaryReserved">$0.00</strong><small id="summaryReservedCount">0 reservas activas.</small></div>
          </div>
        </section>
        <section class="finance-block finance-block-pending">
          <div class="finance-kicker">Pendiente</div>
          <div class="finance-split">
            <div class="finance-metric"><span>Solicitudes sin confirmar</span><strong id="summaryPendingRequests">$0.00</strong><small id="summaryPendingCount">0 solicitudes pendientes.</small></div>
            <div class="finance-metric"><span>Saldo de reservas</span><strong id="summaryReservedBalance">$0.00</strong><small>Por cobrar de reservas activas.</small></div>
          </div>
        </section>
        <div class="finance-note">Caja recibida sí es dinero confirmado. Las solicitudes pendientes no se consideran ingreso hasta que confirmes el pago.</div>
      </div>
'''
replace_once(old_finance, new_finance, 'finance markup')

# 4) Add internal Analysis view after Operating Expenses.
old_tail = '''    <div id="viewGastos" class="view-section hidden">
      <div class="card placeholder-card">
        <span class="placeholder-badge">Módulo preparado</span>
        <h2 style="margin-top:14px;">Gastos Operativos</h2>
        <p class="section-intro" style="margin-bottom:0;">Aquí centralizaremos costos de proveedor, shipping, carga marítima o aérea, publicidad y otros gastos operativos. La estructura financiera se configurará en el siguiente ajuste.</p>
      </div>
    </div>
  </div>
</div>
'''
new_tail = '''    <div id="viewGastos" class="view-section hidden">
      <div class="card placeholder-card">
        <span class="placeholder-badge">Módulo preparado</span>
        <h2 style="margin-top:14px;">Gastos Operativos</h2>
        <p class="section-intro" style="margin-bottom:0;">Aquí centralizaremos costos de proveedor, shipping, carga marítima o aérea, publicidad y otros gastos operativos. La estructura financiera se configurará en el siguiente ajuste.</p>
      </div>
    </div>

    <div id="viewAnalisis" class="view-section hidden">
      <div class="card">
        <div class="analysis-header">
          <div>
            <h2>Análisis de demanda</h2>
            <p class="section-intro">Usa las solicitudes reales para detectar qué productos generan más demanda y dónde el inventario puede quedarse corto.</p>
          </div>
          <div class="analysis-period">
            <label for="analysisWindow">Periodo</label>
            <select id="analysisWindow">
              <option value="30">Últimos 30 días</option>
              <option value="90" selected>Últimos 90 días</option>
              <option value="all">Todo el historial</option>
            </select>
          </div>
        </div>
        <div id="analysisMsg"></div>
        <div class="analysis-summary-line" id="analysisSummaryLine">
          <span>Solicitadas <strong id="analysisRequested">0</strong></span>
          <span>Confirmadas <strong id="analysisConfirmed">0</strong></span>
          <span>Por pedido <strong id="analysisBackorder">0</strong></span>
          <span>Valor solicitado <strong id="analysisValue">$0.00</strong></span>
        </div>
        <div class="demand-chart">
          <h3>Qué se está pidiendo más</h3>
          <div id="demandBars"><p class="helper-text">Aún no hay información suficiente.</p></div>
        </div>
        <div class="table-scroll analysis-scroll">
          <table>
            <thead><tr><th>Producto</th><th>Solicitadas</th><th>Confirmadas</th><th>Pendientes</th><th>Por pedido</th><th>Stock actual</th><th>Lectura</th></tr></thead>
            <tbody id="analysisBody"></tbody>
          </table>
        </div>
        <p class="analysis-note">Confirmadas = Reservadas + Pagadas. Pendientes representan intención, no ingreso. “Por pedido” identifica solicitudes que excedieron el stock disponible al momento de la solicitud. Este módulo orienta reposición; no calcula margen todavía porque los costos operativos aún no están registrados.</p>
      </div>
    </div>
  </div>
</div>
'''
replace_once(old_tail, new_tail, 'analysis view')

# 5) View routing.
replace_once(
'''    proximos: document.getElementById('viewProximos'),
    gastos: document.getElementById('viewGastos')
  };
  const viewLoaded = { solicitudes: true, inventario: false, proximos: false, gastos: true };
''',
'''    proximos: document.getElementById('viewProximos'),
    gastos: document.getElementById('viewGastos'),
    analisis: document.getElementById('viewAnalisis')
  };
  const viewLoaded = { solicitudes: true, inventario: false, proximos: false, gastos: true, analisis: false };
''',
'view routing object')
replace_once(
"    if (view === 'proximos' && !viewLoaded.proximos) { loadUpcoming(); loadDrafts(); viewLoaded.proximos = true; }\n",
"    if (view === 'proximos' && !viewLoaded.proximos) { loadUpcoming(); loadDrafts(); viewLoaded.proximos = true; }\n    if (view === 'analisis') loadAnalysis();\n",
'analysis route load')
replace_once(
"    if (currentView === 'proximos') { loadUpcoming(); loadDrafts(); }\n",
"    if (currentView === 'proximos') { loadUpcoming(); loadDrafts(); }\n    if (currentView === 'analisis') loadAnalysis();\n",
'analysis refresh')

# 6) Finance calculations. Do not combine unconfirmed requests with reservation balances.
pattern = re.compile(r"  async function loadFinancialSummary\(\) \{.*?\n  \}\n\n  async function loadOrders\(status\) \{", re.S)
replacement = r'''  async function loadFinancialSummary() {
    const { data, error } = await client
      .from('orders')
      .select('status, total_reference, amount_paid');
    if (error) {
      console.error('[Prime Drop] Error cargando resumen financiero:', error.message);
      return;
    }

    const active = (data || []).filter(o => ['pending', 'reserved', 'paid'].includes(o.status));
    const pending = active.filter(o => o.status === 'pending');
    const reserved = active.filter(o => o.status === 'reserved');
    const paid = active.filter(o => o.status === 'paid');

    const paidSales = paid.reduce((sum, o) => sum + Number(o.total_reference || 0), 0);
    const activeDeposits = reserved.reduce((sum, o) => sum + Number(o.amount_paid || 0), 0);
    const collected = paidSales + activeDeposits;
    const pendingRequests = pending.reduce((sum, o) => sum + Math.max(0, Number(o.total_reference || 0) - Number(o.amount_paid || 0)), 0);
    const reservedBalance = reserved.reduce((sum, o) => sum + Math.max(0, Number(o.total_reference || 0) - Number(o.amount_paid || 0)), 0);

    document.getElementById('summaryCollected').textContent = moneyFmt(collected);
    document.getElementById('summaryPaidSales').textContent = moneyFmt(paidSales);
    document.getElementById('summaryReserved').textContent = moneyFmt(activeDeposits);
    document.getElementById('summaryPendingRequests').textContent = moneyFmt(pendingRequests);
    document.getElementById('summaryReservedBalance').textContent = moneyFmt(reservedBalance);
    document.getElementById('summaryReservedCount').textContent = `${reserved.length} reserva${reserved.length === 1 ? '' : 's'} activa${reserved.length === 1 ? '' : 's'}.`;
    document.getElementById('summaryPaidCount').textContent = `${paid.length} venta${paid.length === 1 ? '' : 's'} pagada${paid.length === 1 ? '' : 's'}.`;
    document.getElementById('summaryPendingCount').textContent = `${pending.length} solicitud${pending.length === 1 ? '' : 'es'} pendiente${pending.length === 1 ? '' : 's'}.`;
  }

  async function loadOrders(status) {'''
s, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit('finance function replacement failed')

# 7) Operational wording: buttons express an admin action, not a state.
s = s.replace("'Confirmar abono 50%'", "'Confirmar abono'")
s = s.replace('>Completar pago</button>', '>Confirmar saldo</button>')
s = s.replace('<button data-action="pay"', '<button class="action-confirm" data-action="pay"')
s = s.replace("const label = mode === 'deposit' ? 'Abono 50%' : 'Pago completo';", "const label = mode === 'deposit' ? 'Abono' : 'Pago completo';")
s = s.replace("if (type !== 'backorder') return '<span class=\"badge\" style=\"background:#F1F1F1;color:var(--ink-soft);\">Stock</span>';\n    return '<span class=\"badge\" style=\"background:#FDEFE0;color:#9A5B00;\">Por pedido</span>';",
              "if (type !== 'backorder') return '<span class=\"badge badge-stock\">Stock</span>';\n    return '<span class=\"badge badge-backorder\">Por pedido</span>';")

# 8) Analysis logic from existing orders + items + stock. No new DB schema needed.
analysis_js = r'''
  // ---- Análisis de demanda / reposición ----
  function analysisSignal(row) {
    if (row.requested > 0 && row.stock <= 0) return { label: 'Sin stock con demanda', cls: 'signal-critical' };
    if (row.backorder > 0) return { label: 'Pedidos fuera de stock', cls: 'signal-watch' };
    if (row.requested > row.stock) return { label: 'Demanda > stock', cls: 'signal-watch' };
    return { label: 'Stock cubre señal', cls: 'signal-ok' };
  }

  async function loadAnalysis() {
    const msgEl = document.getElementById('analysisMsg');
    const body = document.getElementById('analysisBody');
    const bars = document.getElementById('demandBars');
    if (!msgEl || !body || !bars) return;
    body.innerHTML = '';
    bars.innerHTML = '<p class="helper-text">Cargando análisis…</p>';
    showMsg(msgEl, '', null);

    const [ordersRes, itemsRes, variantsRes, productsRes] = await Promise.all([
      client.from('orders').select('id, status, fulfillment_type, created_at').neq('status', 'cancelled'),
      client.from('order_items').select('order_id, quantity, unit_price, product_variant_id'),
      client.from('product_variants').select('id, product_id'),
      client.from('products').select('id, name, uses_color_variants, color_stock_mode, product_variants(stock_on_hand), product_color_variants(stock_on_hand)')
    ]);

    const firstError = ordersRes.error || itemsRes.error || variantsRes.error || productsRes.error;
    if (firstError) {
      bars.innerHTML = '';
      showMsg(msgEl, 'No se pudo cargar el análisis: ' + firstError.message, 'error');
      return;
    }

    const windowValue = document.getElementById('analysisWindow').value;
    const cutoff = windowValue === 'all' ? null : Date.now() - Number(windowValue) * 86400000;
    const orders = (ordersRes.data || []).filter(o => !cutoff || new Date(o.created_at).getTime() >= cutoff);
    const orderMap = new Map(orders.map(o => [o.id, o]));
    const variantMap = new Map((variantsRes.data || []).map(v => [v.id, v]));
    const productMap = new Map((productsRes.data || []).map(p => [p.id, p]));
    const grouped = new Map();

    (itemsRes.data || []).forEach(item => {
      const order = orderMap.get(item.order_id);
      if (!order) return;
      const variant = variantMap.get(item.product_variant_id);
      if (!variant) return;
      const product = productMap.get(variant.product_id);
      if (!product) return;

      if (!grouped.has(product.id)) {
        const sharedColorStock = product.uses_color_variants && product.color_stock_mode === 'shared_size';
        const stock = product.uses_color_variants && !sharedColorStock
          ? (product.product_color_variants || []).reduce((sum, v) => sum + Number(v.stock_on_hand || 0), 0)
          : (product.product_variants || []).reduce((sum, v) => sum + Number(v.stock_on_hand || 0), 0);
        grouped.set(product.id, { id: product.id, name: product.name, stock, requested:0, confirmed:0, pending:0, backorder:0, value:0 });
      }

      const row = grouped.get(product.id);
      const qty = Number(item.quantity || 0);
      row.requested += qty;
      row.value += qty * Number(item.unit_price || 0);
      if (order.status === 'reserved' || order.status === 'paid') row.confirmed += qty;
      if (order.status === 'pending') row.pending += qty;
      if (order.fulfillment_type === 'backorder') row.backorder += qty;
    });

    const rows = Array.from(grouped.values()).sort((a, b) => {
      const aPressure = (a.stock <= 0 && a.requested > 0 ? 3 : 0) + (a.backorder > 0 ? 2 : 0) + (a.requested > a.stock ? 1 : 0);
      const bPressure = (b.stock <= 0 && b.requested > 0 ? 3 : 0) + (b.backorder > 0 ? 2 : 0) + (b.requested > b.stock ? 1 : 0);
      return bPressure - aPressure || b.requested - a.requested || b.confirmed - a.confirmed;
    });

    const totals = rows.reduce((acc, r) => {
      acc.requested += r.requested; acc.confirmed += r.confirmed; acc.backorder += r.backorder; acc.value += r.value; return acc;
    }, { requested:0, confirmed:0, backorder:0, value:0 });
    document.getElementById('analysisRequested').textContent = totals.requested;
    document.getElementById('analysisConfirmed').textContent = totals.confirmed;
    document.getElementById('analysisBackorder').textContent = totals.backorder;
    document.getElementById('analysisValue').textContent = moneyFmt(totals.value);

    if (!rows.length) {
      bars.innerHTML = '<p class="helper-text">No hay solicitudes no canceladas en este periodo.</p>';
      body.innerHTML = '<tr><td colspan="7" style="color:var(--ink-soft);">Sin datos para analizar.</td></tr>';
      return;
    }

    const maxRequested = Math.max(...rows.map(r => r.requested), 1);
    bars.innerHTML = rows.slice(0, 8).map(r => {
      const width = Math.max(4, (r.requested / maxRequested) * 100);
      return `<div class="demand-row">
        <div class="demand-name" title="${escapeAttr(r.name)}">${escapeAttr(r.name)}</div>
        <div class="demand-track"><div class="demand-fill" style="width:${width}%"></div></div>
        <div class="demand-meta">${r.requested} solicitada${r.requested === 1 ? '' : 's'} · ${r.confirmed} conf.</div>
      </div>`;
    }).join('');

    rows.forEach(r => {
      const signal = analysisSignal(r);
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${escapeAttr(r.name)}</td><td><strong>${r.requested}</strong></td><td>${r.confirmed}</td><td>${r.pending}</td><td>${r.backorder}</td><td>${r.stock}</td><td><span class="signal ${signal.cls}">${signal.label}</span></td>`;
      body.appendChild(tr);
    });
  }

  document.getElementById('analysisWindow').addEventListener('change', loadAnalysis);

'''
marker = '  // ---- Inventario ----\n'
if marker not in s:
    raise SystemExit('analysis JS insertion marker not found')
s = s.replace(marker, analysis_js + marker, 1)

# Sanity checks.
checks = [
    'data-view="analisis"', 'id="viewAnalisis"', 'summaryPendingRequests', 'summaryReservedBalance',
    'Confirmar abono', 'Confirmar saldo', 'function loadAnalysis()', 'analysisSignal(row)', 'button.action-confirm'
]
for c in checks:
    if c not in s:
        raise SystemExit(f'missing expected output: {c}')
if 'summaryReceivable' in s:
    raise SystemExit('old combined receivable metric remains')

p.write_text(s, encoding='utf-8')
print('patched panel-privado.html')
