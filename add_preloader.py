import os
import re

files_to_update = ['index.html', 'catalog.html', 'product_detail.html', 'checkout.html', 'order_confirmation.html']

preloader_style = """
<style id="preloader-style">
        #preloader {
            position: fixed;
            inset: 0;
            background-color: #faf9f6;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: opacity 0.6s ease-out, visibility 0.6s ease-out;
        }
        .dark #preloader { background-color: #1a1c1a; }
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(212, 175, 55, 0.3); /* D4AF37 */
            border-radius: 50%;
            border-top-color: #d4af37;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        body.preloader-active {
            overflow: hidden;
        }
    </style>
"""

preloader_html = """
<!-- Preloader -->
<div id="preloader">
    <div class="spinner"></div>
</div>
"""

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # Inject style
    if '<style id="preloader-style">' not in content:
        content = content.replace('</head>', preloader_style + '\n</head>')

    # Inject html
    if 'id="preloader"' not in content:
        # We need to add it to body. Also add preloader-active class to body
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + preloader_html, content)
        content = re.sub(r'<body class="([^"]+)"', r'<body class="\1 preloader-active"', content)

    with open(filepath, 'w') as f:
        f.write(content)

print("Preloader injected successfully.")
