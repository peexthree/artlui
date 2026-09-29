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

unlocked_slugs = {'upload', 'merge', 'compress'}

encrypted_data = {}

# Extract SVGs from iconsData array
pattern_icon = r'slug:\s*[\'"]([^\'"]+)[\'"].*?svg:\s*`(<svg.*?</svg>)`'
for m in re.finditer(pattern_icon, html, re.DOTALL):
    slug = m.group(1)
    svg_code = m.group(2)
    if slug not in unlocked_slugs:
        encrypted_data[slug] = xor_encrypt(svg_code, KEY)

# Rewrite ENCRYPTED_SVGS in HTML
encrypted_js_str = json.dumps(encrypted_data)
html = re.sub(r'const ENCRYPTED_SVGS\s*=\s*\{.*?\};', f'const ENCRYPTED_SVGS = {encrypted_js_str};', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Updated index.html successfully with {len(encrypted_data)} encrypted SVGs!")
