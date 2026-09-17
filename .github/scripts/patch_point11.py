from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')
original = s

pairs = [
('''    <div class="step"><div class="step-num">01</div><p>Elige tu pieza.</p></div>\n    <div class="step"><div class="step-num">02</div><p>Consulta disponibilidad por Instagram.</p></div>\n    <div class="step"><div class="step-num">03</div><p>Coordina tu compra directamente con Prime Drop.</p></div>''',
 '''    <div class="step"><div class="step-num">01</div><p>Elige tu pieza, talla y color cuando aplique.</p></div>\n    <div class="step"><div class="step-num">02</div><p>Prepara tu solicitud desde el catálogo.</p></div>\n    <div class="step"><div class="step-num">03</div><p>Envía el mensaje a @primedrop.pa para confirmar pago y entrega.</p></div>'''),
('''      <button class="purchase-submit" id="purchaseSubmit">Continuar</button>''',
 '''      <button class="purchase-submit" id="purchaseSubmit">Preparar mensaje</button>'''),
('''      <p class="purchase-eyebrow">Solicitud creada</p>\n      <h3 id="purchaseSuccessCode">PD-2026-0000</h3>''',
 '''      <p class="purchase-eyebrow">Mensaje listo</p>\n      <h3 id="purchaseSuccessCode">PD-2026-0000</h3>\n      <p class="purchase-instruction">Tu selección quedó registrada. Envía el mensaje a <strong>@primedrop.pa</strong> para continuar la compra.</p>'''),
('''      submitBtn.textContent = availableSizes.length === 0 ? 'No disponible' : 'Continuar';''',
 '''      submitBtn.textContent = availableSizes.length === 0 ? 'No disponible' : 'Preparar mensaje';'''),
('''      window.open(PRIME_DROP_CONFIG.INSTAGRAM_URL, '_blank', 'noopener');\n\n      loadCatalog(); // refresca el stock mostrado (aún no se descontó, pero puede haber cambiado por otra solicitud)''',
 '''      // Instagram se abre únicamente cuando la persona toca el CTA explícito.\n      // Evita ventanas emergentes inesperadas y mantiene claro que la compra\n      // se termina por conversación en @primedrop.pa.\n      loadCatalog(); // refresca el stock mostrado (aún no se descontó, pero puede haber cambiado por otra solicitud)''')
]
for old, new in pairs:
    if old not in s:
        raise SystemExit('Expected Point 11 anchor not found:\n' + old[:180])
    s = s.replace(old, new, 1)

# Replace every reset label still using the vague "Continuar".
if "submitBtn.textContent = 'Continuar';" not in s:
    raise SystemExit('Submit reset labels not found')
s = s.replace("submitBtn.textContent = 'Continuar';", "submitBtn.textContent = 'Preparar mensaje';")

# The pre-RPC loading label varied in prior iterations. Replace the first label
# immediately after submitBtn.disabled = true without depending on its old copy.
pattern = re.compile(r"(\s+submitBtn\.disabled = true;\n\s+submitBtn\.textContent = )'[^']+';")
s, count = pattern.subn(r"\1'Preparando mensaje…';", s, count=1)
if count != 1:
    raise SystemExit(f'Could not identify loading label after submit disable: {count}')

# Re-copy the current message when the explicit Instagram CTA is tapped.
anchor = '''    copyAgainBtn.addEventListener('click', async () => {\n      const ok = await copyMessage(lastMessage);\n      copyAgainBtn.textContent = ok ? '¡Copiado!' : 'No se pudo copiar — selecciona el texto de arriba';\n      setTimeout(() => { copyAgainBtn.textContent = 'Copiar mensaje de nuevo'; }, 2000);\n    });\n'''
insert = anchor + '''\n    document.getElementById('purchaseIgLink').addEventListener('click', () => {\n      if (lastMessage) copyMessage(lastMessage);\n    });\n'''
if anchor not in s:
    raise SystemExit('Instagram CTA handler anchor not found')
s = s.replace(anchor, insert, 1)

required = [
    'Preparar mensaje',
    'Preparando mensaje…',
    'Mensaje listo',
    'Tu selección quedó registrada.',
    'Instagram se abre únicamente cuando la persona toca el CTA explícito.',
    "document.getElementById('purchaseIgLink').addEventListener('click'",
    'Envía el mensaje a @primedrop.pa para confirmar pago y entrega.'
]
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit(f'Point 11 validation failed: {missing}')

# The only remaining automatic Instagram open must be the fallback used when
# Supabase is unavailable; the normal purchase flow must be explicit/user-led.
occurrences = s.count("window.open(PRIME_DROP_CONFIG.INSTAGRAM_URL, '_blank', 'noopener');")
if occurrences != 1:
    raise SystemExit(f'Unexpected Instagram auto-open count: {occurrences}')

if s == original:
    raise SystemExit('No Point 11 changes produced')
path.write_text(s, encoding='utf-8')
