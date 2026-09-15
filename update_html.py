import re
import json
import base64

KEY = "PDFOK-PRO-2026"

def xor_encrypt(text, key):
    encoded_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    res = bytearray()
    for i, b in enumerate(encoded_bytes):
        res.append(b ^ key_bytes[i % len(key_bytes)])
    return base64.b64encode(res).decode('utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update card headers and buttons for locked items
unlocked_slugs = {'upload', 'merge', 'compress'}

# Extract SVGs and generate encrypted map
pattern = r'<svg[^>]*id=\"svg-([^\"]+)\"[^>]*>(.*?)</svg>'
matches = re.findall(pattern, html, re.DOTALL)

encrypted_data = {}
for slug, inner_content in matches:
    if slug not in unlocked_slugs:
        full_svg = f'<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" id="svg-{slug}">{inner_content}</svg>'
        encrypted_data[slug] = xor_encrypt(full_svg, KEY)

# Modify HTML cards for locked items to show lock icons
def modify_card(match):
    full_card = match.group(0)
    slug_match = re.search(r'data-slug="([^"]+)"', full_card)
    if not slug_match:
        return full_card
    slug = slug_match.group(1)

    if slug not in unlocked_slugs:
        # Add lock icon badge to header if not present
        if 'lock-badge' not in full_card:
            full_card = re.sub(
                r'(<span class="text-slate-400 text-\[11px\]">№\d+ · [^<]+</span>)',
                r'\1 <span class="lock-badge inline-flex items-center text-amber-500 font-semibold ml-1" title="Требуется активация"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg></span>',
                full_card
            )
    return full_card

card_pattern = r'<div class="preview-card border rounded-2xl p-4 flex flex-col transition" data-cat="[^"]+" data-slug="[^"]+">.*?(?=<div class="preview-card|</div>\s*</main>)'
html = re.sub(card_pattern, modify_card, html, flags=re.DOTALL)

# Add Modal HTML before Toast
modal_html = """
  <!-- Модальное окно активации Kwork -->
  <div id="activation-modal" class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 opacity-0 pointer-events-none transition-opacity duration-300">
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl transform scale-95 transition-transform duration-300 id-modal-box">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center font-bold">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          </div>
          <div>
            <h3 class="text-base font-bold text-slate-900 dark:text-slate-100">Активация экспортного пакета</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">PDFok · Все 32 SVG анимации</p>
          </div>
        </div>
        <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-lg p-1">&times;</button>
      </div>

      <div class="mb-5 text-xs text-slate-600 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-slate-800/50 p-3.5 rounded-xl border border-slate-100 dark:border-slate-800">
        Для поштучного скачивания remaining 29 SVG и выгрузки полного ZIP-архива введите ключ активации проекта (выдается после принятия этапа и оплаты на Kwork).
      </div>

      <form onsubmit="handleActivation(event)" class="space-y-4">
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Ключ активации:</label>
          <input type="text" id="activation-key-input" placeholder="например, PDFOK-PRO-2026" class="w-full px-3.5 py-2.5 text-xs rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-500 font-mono tracking-wider uppercase transition">
          <p id="activation-error" class="text-[11px] text-red-500 font-medium mt-1.5 hidden">Неверный ключ активации. Проверьте правильность ввода.</p>
        </div>

        <div class="flex items-center gap-2 pt-2">
          <button type="button" onclick="closeModal()" class="flex-1 text-xs py-2.5 px-4 border border-slate-200 dark:border-slate-700 rounded-xl font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition">Отмена</button>
          <button type="submit" class="flex-1 text-xs py-2.5 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-xl font-bold shadow-sm transition">Активировать</button>
        </div>
      </form>
    </div>
  </div>
"""

html = html.replace('<!-- Уведомление -->', modal_html + '\n  <!-- Уведомление -->')

# Now rewrite JS script section
encrypted_js_str = json.dumps(encrypted_data)

js_replacement = f"""<script>
    const UNLOCKED_PILOTS = new Set(['upload', 'merge', 'compress']);
    const ENCRYPTED_SVGS = {encrypted_js_str};

    function isActivated() {{
      return sessionStorage.getItem('pdfok_activated') === 'true';
    }}

    function xorDecrypt(b64Str, key) {{
      try {{
        const binary = atob(b64Str);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {{
          bytes[i] = binary.charCodeAt(i);
        }}
        const keyBytes = new TextEncoder().encode(key);
        const decrypted = new Uint8Array(bytes.length);
        for (let i = 0; i < bytes.length; i++) {{
          decrypted[i] = bytes[i] ^ keyBytes[i % keyBytes.length];
        }}
        return new TextDecoder().decode(decrypted);
      }} catch (e) {{
        return null;
      }}
    }}

    function openModal() {{
      const modal = document.getElementById('activation-modal');
      const box = modal.querySelector('.id-modal-box');
      modal.classList.remove('opacity-0', 'pointer-events-none');
      box.classList.remove('scale-95');
      box.classList.add('scale-100');
      document.getElementById('activation-key-input').focus();
    }}

    function closeModal() {{
      const modal = document.getElementById('activation-modal');
      const box = modal.querySelector('.id-modal-box');
      box.classList.remove('scale-100');
      box.classList.add('scale-95');
      modal.classList.add('opacity-0', 'pointer-events-none');
      document.getElementById('activation-error').classList.add('hidden');
      document.getElementById('activation-key-input').value = '';
    }}

    function handleActivation(e) {{
      e.preventDefault();
      const input = document.getElementById('activation-key-input');
      const val = input.value.trim().toUpperCase();
      const errorEl = document.getElementById('activation-error');

      if (val === 'PDFOK-PRO-2026') {{
        sessionStorage.setItem('pdfok_activated', 'true');
        closeModal();
        updateUIState();
        showToast('Проект успешно активирован! Весь экспорт разблокирован.');
      }} else {{
        errorEl.classList.remove('hidden');
      }}
    }}

    function updateUIState() {{
      const activated = isActivated();
      const badges = document.querySelectorAll('.lock-badge');
      badges.forEach(b => {{
        b.style.display = activated ? 'none' : 'inline-flex';
      }});
    }}

    // Переключение тем сайта PDFok (#0f766e vs #2dd4bf)
    function setTheme(theme) {{
      const body = document.body;
      const btnLight = document.getElementById('btn-light');
      const btnDark = document.getElementById('btn-dark');

      if (theme === 'dark') {{
        body.classList.remove('theme-light');
        body.classList.add('theme-dark');
        btnDark.className = 'px-2.5 py-1 text-xs font-semibold rounded-md transition-all bg-slate-700 text-teal-300 shadow-xs';
        btnLight.className = 'px-2.5 py-1 text-xs font-medium rounded-md transition-all text-slate-400';
      }} else {{
        body.classList.remove('theme-dark');
        body.classList.add('theme-light');
        btnLight.className = 'px-2.5 py-1 text-xs font-semibold rounded-md transition-all bg-white text-teal-800 shadow-xs';
        btnDark.className = 'px-2.5 py-1 text-xs font-medium rounded-md transition-all text-slate-600';
      }}
    }}

    // Тест первого кадра (проверка требования ТЗ: у части людей анимация выключена)
    let isFrozen = false;
    function toggleFreeze() {{
      isFrozen = !isFrozen;
      document.body.classList.toggle('freeze-animations', isFrozen);
      const dot = document.getElementById('freeze-dot');
      const label = document.getElementById('freeze-label');
      if (isFrozen) {{
        dot.className = 'w-2 h-2 rounded-full bg-emerald-500 animate-pulse';
        label.innerText = 'Возобновить анимацию';
        showToast('Анимация заморожена: тест статичного 1-го кадра');
      }} else {{
        dot.className = 'w-2 h-2 rounded-full bg-amber-500';
        label.innerText = 'Стоп (тест 1-го кадра)';
        showToast('Анимации возобновлены');
      }}
    }}

    // Фильтрация карточек по категориям
    function filterCategory(cat, btn) {{
      document.querySelectorAll('.filter-btn').forEach(b => {{
        b.className = 'filter-btn px-2.5 py-1 rounded-md font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition';
      }});
      btn.className = 'filter-btn active px-2.5 py-1 rounded-md font-semibold bg-teal-700 text-white dark:bg-teal-400 dark:text-slate-950 transition';

      const cards = document.querySelectorAll('#cards-container > div');
      cards.forEach(card => {{
        if (cat === 'all' || card.getAttribute('data-cat') === cat) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // Извлечение чистого XML-кода SVG
    function getCleanSvg(slug) {{
      if (UNLOCKED_PILOTS.has(slug)) {{
        const el = document.getElementById('svg-' + slug);
        return el ? el.outerHTML : '';
      }}
      if (isActivated()) {{
        if (ENCRYPTED_SVGS[slug]) {{
          const decrypted = xorDecrypt(ENCRYPTED_SVGS[slug], 'PDFOK-PRO-2026');
          if (decrypted) return decrypted;
        }}
        const el = document.getElementById('svg-' + slug);
        return el ? el.outerHTML : '';
      }}
      return null;
    }}

    // Копирование в буфер обмена
    function copySvg(slug) {{
      if (!UNLOCKED_PILOTS.has(slug) && !isActivated()) {{
        openModal();
        return;
      }}
      const svgCode = getCleanSvg(slug);
      if (!svgCode) return;

      const textarea = document.createElement('textarea');
      textarea.value = svgCode;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      try {{
        document.execCommand('copy');
        showToast('Код ' + slug + '.svg скопирован в буфер!');
      }} catch (e) {{
        showToast('Не удалось скопировать код');
      }}
      document.body.removeChild(textarea);
    }}

    // Поштучное скачивание .svg файла
    function downloadSvg(slug) {{
      if (!UNLOCKED_PILOTS.has(slug) && !isActivated()) {{
        openModal();
        return;
      }}
      const svgCode = getCleanSvg(slug);
      if (!svgCode) return;

      const blob = new Blob([svgCode], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = slug + '.svg';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('Файл ' + slug + '.svg скачан!');
    }}

    // Скачивание ВСЕХ 32 SVG одним ZIP-архивом
    async function downloadAllZip() {{
      if (!isActivated()) {{
        openModal();
        return;
      }}
      const btn = document.getElementById('btn-zip');
      const origText = btn.innerHTML;
      btn.innerHTML = `
        <svg class="animate-spin w-3.5 h-3.5" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>
        <span>Упаковка ZIP...</span>
      `;
      btn.disabled = true;

      try {{
        const zip = new JSZip();
        const cards = document.querySelectorAll('#cards-container > div');
        let count = 0;

        cards.forEach(card => {{
          const slug = card.getAttribute('data-slug');
          const code = getCleanSvg(slug);
          if (slug && code) {{
            zip.file(slug + '.svg', code);
            count++;
          }}
        }});

        zip.file('README.txt',
`PDFok · Комплект из ${{count}} анимированных SVG
------------------------------------------------------
Параметры:
- Холст: viewBox="0 0 160 100" (без width/height)
- Линии: stroke-width 2-2.5px, stroke-linecap="round"
- Цвета: stroke="currentColor", fill="currentColor"
- Бумага: #ffffff
- Автономный CSS @keyframes в <style>
- Уникальные префиксы классов и @keyframes по слагам
- Поддержка prefers-reduced-motion
`);

        const content = await zip.generateAsync({{ type: 'blob' }});
        const url = URL.createObjectURL(content);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'PDFok_all_32_svg_animations.zip';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast('Все 32 SVG успешно упакованы в ZIP!');
      }} catch (err) {{
        showToast('Ошибка при сборке ZIP-архива');
      }} finally {{
        btn.innerHTML = origText;
        btn.disabled = false;
      }}
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      const text = document.getElementById('toast-text');
      text.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2500);
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      updateUIState();
    }});
  </script>"""

html = re.sub(r'<script>.*?</script>', js_replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
