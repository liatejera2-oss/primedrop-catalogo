from pathlib import Path
p=Path("panel-privado.html")
s=p.read_text(encoding="utf-8")

css_anchor="  @media (max-width:900px) {\n"
css="""  .manual-sale-grid { display:grid; grid-template-columns:minmax(190px,1.5fr) 150px 120px 90px 150px auto; gap:10px; align-items:end; }
  .manual-sale-grid label { margin-bottom:5px; }
  .manual-sale-grid input, .manual-sale-grid select { width:100%; margin:0; }
  .manual-sale-hint { margin-top:10px; color:var(--ink-soft); font-size:11.5px; line-height:1.45; }
  @media (max-width:980px) { .manual-sale-grid { grid-template-columns:repeat(3,minmax(0,1fr)); } }
  @media (max-width:700px) { .manual-sale-grid { grid-template-columns:1fr; } }
"""
assert css_anchor in s
s=s.replace(css_anchor,css+css_anchor,1)

html_anchor="""        <p class="section-intro">Gestiona cada solicitud según el pago recibido. Los cambios de estado actualizan la reserva y el inventario automáticamente.</p>
"""
html_block=html_anchor+"""        <details class="policy-details" id="manualSaleDetails">
          <summary>Registrar venta directa</summary>
          <div class="details-body">
            <p style="margin-bottom:12px;">Para ventas que comenzaron directamente por Instagram. Regístrala solo cuando ya recibiste el pago completo o el abono.</p>
            <div id="manualSaleMsg"></div>
            <div class="manual-sale-grid">
              <div><label for="manualSaleProduct">Producto</label><select id="manualSaleProduct"></select></div>
              <div id="manualSaleColorField" class="hidden"><label for="manualSaleColor">Color</label><select id="manualSaleColor"></select></div>
              <div><label for="manualSaleSize">Talla</label><select id="manualSaleSize"></select></div>
              <div><label for="manualSaleQty">Cantidad</label><input type="number" min="1" step="1" id="manualSaleQty" value="1"></div>
              <div><label for="manualSalePayment">Pago</label><select id="manualSalePayment"><option value="full">Pago completo</option><option value="deposit">Abono 50%</option></select></div>
              <button class="action-confirm" id="manualSaleBtn">Registrar venta</button>
            </div>
            <p class="manual-sale-hint" id="manualSaleHint"></p>
          </div>
        </details>
"""
assert html_anchor in s
s=s.replace(html_anchor,html_block,1)

s=s.replace("    loadFinancialSummary();\n", "    loadFinancialSummary();\n    loadManualSaleProducts();\n", 1)
s=s.replace("    if (currentView === 'solicitudes') { loadOrders(activeStatus); loadFinancialSummary(); }", "    if (currentView === 'solicitudes') { loadOrders(activeStatus); loadFinancialSummary(); loadManualSaleProducts(); }", 1)

js_anchor="  // ---- Solicitudes ----\n"
js=r'''  // ---- Venta manual desde Instagram ----
  let manualSaleProducts = [];

  async function loadManualSaleProducts() {
    const select = document.getElementById('manualSaleProduct');
    if (!select) return;
    const { data, error } = await client.from('products')
      .select('slug,name,active,sale_mode,regular_price,preorder_price,uses_color_variants,color_stock_mode,published_once,is_upcoming,product_variants(size,stock_on_hand),product_color_variants(color,size,stock_on_hand)')
      .eq('published_once', true)
      .eq('is_upcoming', false)
      .order('name');

    if (error) {
      select.innerHTML = '<option value="">No se pudo cargar</option>';
      return;
    }

    manualSaleProducts = data || [];
    select.innerHTML = manualSaleProducts.map(function(p) {
      return '<option value="' + escapeAttr(p.slug) + '">' + escapeAttr(p.name) + (p.active ? '' : ' · oculto') + '</option>';
    }).join('');

    renderManualSaleOptions();
  }

  function selectedManualProduct() {
    const slug = document.getElementById('manualSaleProduct')?.value;
    return manualSaleProducts.find(function(p) { return p.slug === slug; }) || null;
  }

  function manualStockFor(p, color, size) {
    if (!p) return 0;
    if (p.sale_mode === 'preorder') return 0;
    if (p.uses_color_variants && p.color_stock_mode === 'per_color') {
      const v = (p.product_color_variants || []).find(function(x) { return x.color === color && x.size === size; });
      return Number(v?.stock_on_hand || 0);
    }
    const v = (p.product_variants || []).find(function(x) { return x.size === size; });
    return Number(v?.stock_on_hand || 0);
  }

  function updateManualSaleHint() {
    const p = selectedManualProduct();
    const hint = document.getElementById('manualSaleHint');
    if (!p || !hint) return;
    const color = document.getElementById('manualSaleColor')?.value || '';
    const size = document.getElementById('manualSaleSize')?.value || '';
    const qty = Math.max(1, parseInt(document.getElementById('manualSaleQty')?.value, 10) || 1);
    const stock = manualStockFor(p, color, size);
    const price = p.sale_mode === 'preorder' ? p.preorder_price : p.regular_price;
    if (p.sale_mode === 'preorder' || stock < qty) {
      hint.textContent = 'Se registrará como Por pedido · ' + moneyFmt(Number(price || 0) * qty) + '.';
    } else {
      hint.textContent = 'Stock disponible: ' + stock + ' · Total: ' + moneyFmt(Number(price || 0) * qty) + '.';
    }
  }

  function renderManualSaleOptions() {
    const p = selectedManualProduct();
    const colorField = document.getElementById('manualSaleColorField');
    const colorSelect = document.getElementById('manualSaleColor');
    const sizeSelect = document.getElementById('manualSaleSize');
    if (!p || !colorField || !colorSelect || !sizeSelect) return;

    const sizes = ['S','M','L','XL'].filter(function(size) {
      return (p.product_variants || []).some(function(v) { return v.size === size; });
    });

    if (p.uses_color_variants) {
      const colors = Array.from(new Set((p.product_color_variants || []).map(function(v) { return v.color; })));
      colorField.classList.remove('hidden');
      colorSelect.innerHTML = colors.map(function(c) { return '<option value="' + escapeAttr(c) + '">' + escapeAttr(c) + '</option>'; }).join('');
    } else {
      colorField.classList.add('hidden');
      colorSelect.innerHTML = '';
    }

    sizeSelect.innerHTML = sizes.map(function(size) {
      const c = colorSelect.value || '';
      const stock = manualStockFor(p, c, size);
      return '<option value="' + size + '">' + size + ' · ' + (p.sale_mode === 'preorder' ? 'por encargo' : stock + ' disp.') + '</option>';
    }).join('');
    updateManualSaleHint();
  }

  document.getElementById('manualSaleProduct').addEventListener('change', renderManualSaleOptions);
  document.getElementById('manualSaleColor').addEventListener('change', renderManualSaleOptions);
  document.getElementById('manualSaleSize').addEventListener('change', updateManualSaleHint);
  document.getElementById('manualSaleQty').addEventListener('input', updateManualSaleHint);

  document.getElementById('manualSaleBtn').addEventListener('click', async function() {
    const btn = document.getElementById('manualSaleBtn');
    const msg = document.getElementById('manualSaleMsg');
    const p = selectedManualProduct();
    if (!p) { showMsg(msg, 'Selecciona un producto.', 'error'); return; }

    const color = p.uses_color_variants ? document.getElementById('manualSaleColor').value : null;
    const size = document.getElementById('manualSaleSize').value;
    const qty = Math.max(0, parseInt(document.getElementById('manualSaleQty').value,10) || 0);
    const payment = document.getElementById('manualSalePayment').value;
    if (!size || qty < 1) { showMsg(msg, 'Revisa talla y cantidad.', 'error'); return; }

    const actionName = payment === 'deposit' ? 'abono' : 'pago completo';
    if (!confirm('Registrar venta directa de ' + p.name + ' con ' + actionName + '?\n\nEsta acción actualizará caja y stock cuando corresponda.')) return;

    btn.disabled = true;
    const { data, error } = await client.rpc('create_manual_sale', {
      p_product_slug: p.slug,
      p_size: size,
      p_color: color,
      p_quantity: qty,
      p_payment_mode: payment
    });
    btn.disabled = false;

    if (error) { showMsg(msg, error.message, 'error'); return; }
    const row = Array.isArray(data) ? data[0] : data;
    const statusLabel = row?.status === 'reserved' ? 'Reservada' : 'Pagada';
    const typeLabel = row?.fulfillment_type === 'backorder' ? ' · Por pedido' : '';
    showMsg(msg, 'Venta ' + row.order_number + ' registrada como ' + statusLabel + typeLabel + '. Total: ' + moneyFmt(row.total_reference) + '.', 'ok');
    document.getElementById('manualSaleQty').value = 1;
    loadOrders(activeStatus);
    loadFinancialSummary();
    loadInventory();
    loadManualSaleProducts();
    if (viewLoaded.analisis) loadAnalysis();
  });

'''
assert js_anchor in s
s=s.replace(js_anchor,js+js_anchor,1)

p.write_text(s,encoding="utf-8")
print("Manual sales patch applied")
