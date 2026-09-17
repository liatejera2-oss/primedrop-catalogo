from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css_anchor="  .visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }\n"
css_add=css_anchor+"""  .skip-link { position:fixed; top:10px; left:10px; z-index:999; transform:translateY(-160%); background:var(--ink); color:#fff; padding:10px 14px; border-radius:8px; font-size:13px; font-weight:700; text-decoration:none; transition:transform .15s ease; }
  .skip-link:focus { transform:translateY(0); }
"""
assert css_anchor in s
s=s.replace(css_anchor,css_add,1)

s=s.replace('<body>\n','<body>\n<a class="skip-link" href="#catalogo">Ir al catálogo</a>\n',1)
s=s.replace('<div class="purchase-overlay" id="purchaseModal" role="dialog" aria-modal="true" aria-labelledby="purchaseTitle">','<div class="purchase-overlay" id="purchaseModal" role="dialog" aria-modal="true" aria-labelledby="purchaseTitle" aria-hidden="true">',1)
s=s.replace('<div id="purchaseStepSuccess" hidden>','<div id="purchaseStepSuccess" aria-live="polite" hidden>',1)
s=s.replace('<h3 id="purchaseSuccessCode">','<h3 id="purchaseSuccessCode" tabindex="-1">',1)
s=s.replace('<p class="purchase-stock-note" id="purchaseStockNote"></p>','<p class="purchase-stock-note" id="purchaseStockNote" role="status" aria-live="polite"></p>',1)
s=s.replace('<div class="lightbox-overlay" id="lightbox" role="dialog" aria-modal="true" aria-label="Foto ampliada del producto">','<div class="lightbox-overlay" id="lightbox" role="dialog" aria-modal="true" aria-label="Foto ampliada del producto" aria-hidden="true">',1)
# Supabase must execute before the inline catalog code that immediately follows it.
s=s.replace('<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js" defer></script>','<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>',1)

trap_anchor='''  // Lightbox / zoom on product photos
  (function () {'''
trap_code='''  function trapFocusWithin(event, container) {
    if (event.key !== 'Tab') return;
    const focusable = Array.from(container.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'))
      .filter(el => !el.hidden && el.offsetParent !== null && getComputedStyle(el).visibility !== 'hidden');
    if (!focusable.length) { event.preventDefault(); return; }
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }

  // Lightbox / zoom on product photos
  (function () {'''
assert trap_anchor in s
s=s.replace(trap_anchor,trap_code,1)

s=s.replace("      overlay.classList.add('open');\n      closeBtn.focus();", "      overlay.classList.add('open');\n      overlay.setAttribute('aria-hidden', 'false');\n      closeBtn.focus();",1)
s=s.replace("      overlay.classList.remove('open');\n      document.body.style.overflow = '';\n      if (lastFocused) lastFocused.focus();", "      overlay.classList.remove('open');\n      overlay.setAttribute('aria-hidden', 'true');\n      document.body.style.overflow = '';\n      if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();",1)

light_key_old='''    document.addEventListener('keydown', (e) => {
      if (!overlay.classList.contains('open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') goPrev();
      if (e.key === 'ArrowRight') goNext();
    });'''
light_key_new='''    document.addEventListener('keydown', (e) => {
      if (!overlay.classList.contains('open')) return;
      if (e.key === 'Escape') { e.preventDefault(); closeLightbox(); return; }
      if (e.key === 'ArrowLeft') { e.preventDefault(); goPrev(); return; }
      if (e.key === 'ArrowRight') { e.preventDefault(); goNext(); return; }
      trapFocusWithin(e, overlay);
    });'''
assert light_key_old in s
s=s.replace(light_key_old,light_key_new,1)

load_error_old='''      if (error) {
        console.error('[Prime Drop] Error cargando el catálogo desde Supabase:', error.message);
        return;
      }

      catalog = {};'''
load_error_new='''      if (error) {
        console.error('[Prime Drop] Error cargando el catálogo desde Supabase:', error.message);
        document.querySelectorAll('.size-row[data-dynamic="true"]').forEach(row => {
          row.innerHTML = '<span class="size-loading">No pudimos cargar la disponibilidad. Recarga la página.</span>';
        });
        purchaseButtons.forEach(btn => {
          btn.disabled = true;
          btn.setAttribute('aria-disabled', 'true');
        });
        return;
      }

      purchaseButtons.forEach(btn => {
        btn.disabled = false;
        btn.removeAttribute('aria-disabled');
      });
      catalog = {};'''
assert load_error_old in s
s=s.replace(load_error_old,load_error_new,1)

state_anchor="    let lastMessage = '';\n"
assert state_anchor in s
s=s.replace(state_anchor,state_anchor+"    let lastPurchaseFocus = null;\n",1)

open_anchor='''    function openModal(slug) {
      const product = catalog[slug];
      if (!product) return;
      currentSlug = slug;'''
open_repl='''    function openModal(slug) {
      const product = catalog[slug];
      if (!product) return;
      lastPurchaseFocus = document.activeElement;
      currentSlug = slug;'''
assert open_anchor in s
s=s.replace(open_anchor,open_repl,1)

open_end="""      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }
"""
open_end_repl="""      overlay.classList.add('open');
      overlay.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      requestAnimationFrame(() => closeBtn.focus());
    }

    function closeModal() {
      overlay.classList.remove('open');
      overlay.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (lastPurchaseFocus && typeof lastPurchaseFocus.focus === 'function') lastPurchaseFocus.focus();
    }
"""
assert open_end in s
s=s.replace(open_end,open_end_repl,1)

copy_pattern=re.compile(r"    async function copyMessage\(msg\) \{.*?\n    \}\n\n    colorsEl\.addEventListener",re.S)
m=copy_pattern.search(s)
assert m,'copyMessage block missing'
copy_repl='''    async function copyMessage(msg) {
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(msg);
          return true;
        } catch (e) {
          console.warn('[Prime Drop] Clipboard API no disponible; usando copia compatible.', e);
        }
      }
      try {
        const textarea = document.createElement('textarea');
        textarea.value = msg;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        textarea.style.pointerEvents = 'none';
        document.body.appendChild(textarea);
        textarea.select();
        textarea.setSelectionRange(0, textarea.value.length);
        const copied = document.execCommand('copy');
        textarea.remove();
        return copied;
      } catch (e) {
        console.warn('[Prime Drop] No se pudo copiar el mensaje.', e);
        return false;
      }
    }

    colorsEl.addEventListener'''
s=s[:m.start()]+copy_repl+s[m.end():]

purchase_key_old="    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && overlay.classList.contains('open')) closeModal(); });"
purchase_key_new="""    document.addEventListener('keydown', (e) => {
      if (!overlay.classList.contains('open')) return;
      if (e.key === 'Escape') { e.preventDefault(); closeModal(); return; }
      trapFocusWithin(e, overlay);
    });"""
assert purchase_key_old in s
s=s.replace(purchase_key_old,purchase_key_new,1)

busy_anchor="""      submitBtn.disabled = true;
      submitBtn.textContent = 'Preparando mensaje…';
      errorEl.hidden = true;
"""
busy_repl="""      submitBtn.disabled = true;
      submitBtn.setAttribute('aria-busy', 'true');
      submitBtn.textContent = 'Preparando mensaje…';
      errorEl.hidden = true;
"""
assert busy_anchor in s
s=s.replace(busy_anchor,busy_repl,1)

busy_done="""      submitBtn.disabled = false;
      submitBtn.textContent = 'Preparar mensaje';

      if (error) {"""
busy_done_repl="""      submitBtn.disabled = false;
      submitBtn.removeAttribute('aria-busy');
      submitBtn.textContent = 'Preparar mensaje';

      if (error) {"""
assert busy_done in s
s=s.replace(busy_done,busy_done_repl,1)

success_anchor="""      messageBoxEl.textContent = message;

      // Instagram se abre únicamente"""
success_repl="""      messageBoxEl.textContent = message;
      requestAnimationFrame(() => successCodeEl.focus({ preventScroll: true }));

      // Instagram se abre únicamente"""
assert success_anchor in s
s=s.replace(success_anchor,success_repl,1)

p.write_text(s,encoding='utf-8')
print('Point 16 patched')
