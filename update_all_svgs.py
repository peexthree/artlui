import re
import json

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Helper to construct SVG string cleanly
def build_svg(slug, style_css, inner_content):
    return f'<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" id="svg-{slug}"><style>@media(prefers-reduced-motion:reduce){{#svg-{slug} *{{animation:none!important}}}}' + style_css + f'</style><g transform="translate(40.4, 10.4) scale(1.65)">' + inner_content + '</g></svg>'

# Keyframes for standard 9 converters (unified scheme)
CONVERTER_CSS_FORWARD = '''.{prefix}-src{{animation:{prefix}-s 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:19.2px 19.2px}}
.{prefix}-arr{{animation:{prefix}-a 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:32px 32px}}
.{prefix}-target{{animation:{prefix}-t 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:28.8px 28.8px}}
@keyframes {prefix}-s{{0%,20%{{transform:translate(0,0) scale(1)}}25%{{transform:translate(-2px,-2px) scale(0.95)}}38%{{transform:translate(3px,3px) scale(1.03)}}60%,80%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(0,0) scale(1)}}}}
@keyframes {prefix}-a{{0%,20%{{transform:translate(0,0) scale(1)}}26%{{transform:translate(-3px,-3px) scale(0.9)}}38%{{transform:translate(6px,6px) scale(1.1)}}52%{{transform:translate(4px,4px) scale(1.01)}}60%,80%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(0,0) scale(1)}}}}
@keyframes {prefix}-t{{0%,36%{{transform:translate(0,0) scale(1)}}44%{{transform:translate(3px,3px) scale(1.1,0.9)}}52%{{transform:translate(-1px,-1px) scale(0.92,1.08)}}60%,80%{{transform:translate(0,0) scale(1.01,0.99)}}100%{{transform:translate(0,0) scale(1)}}}}'''

CONVERTER_CSS_REVERSE = '''.{prefix}-src{{animation:{prefix}-s 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:19.2px 19.2px}}
.{prefix}-arr{{animation:{prefix}-a 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:12px 12px}}
.{prefix}-target{{animation:{prefix}-t 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:28.8px 28.8px}}
@keyframes {prefix}-s{{0%,20%{{transform:translate(0,0) scale(1)}}25%{{transform:translate(-2px,-2px) scale(0.95)}}38%{{transform:translate(3px,3px) scale(1.03)}}60%,80%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(0,0) scale(1)}}}}
@keyframes {prefix}-a{{0%,20%{{transform:translate(0,0) scale(1)}}26%{{transform:translate(3px,3px) scale(0.9)}}38%{{transform:translate(-6px,-6px) scale(1.1)}}52%{{transform:translate(-4px,-4px) scale(1.01)}}60%,80%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(0,0) scale(1)}}}}
@keyframes {prefix}-t{{0%,36%{{transform:translate(0,0) scale(1)}}44%{{transform:translate(-3px,-3px) scale(1.1,0.9)}}52%{{transform:translate(1px,1px) scale(0.92,1.08)}}60%,80%{{transform:translate(0,0) scale(1.01,0.99)}}100%{{transform:translate(0,0) scale(1)}}}}'''

# Dictionary of updated SVGs
svgs = {}

# 1. WORD-TO-PDF
svgs['word-to-pdf'] = build_svg('word-to-pdf',
CONVERTER_CSS_FORWARD.format(prefix='wp'),
'''<g class="wp-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="wp-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#22C55E"/><path d="M10.153 14.232a1.8 1.8 0 1 1 3.501-.829l1.893 8.389 2.403-7.383a1.404 1.404 0 0 1 2.67 0l2.403 7.383 1.913-8.48a1.681 1.681 0 1 1 3.258.828l-2.985 10.54a2.364 2.364 0 0 1-4.475.221l-1.79-4.549-1.8 4.576a2.322 2.322 0 0 1-4.413-.291z" fill="#ffffff"/></g><g class="wp-arr"><path d="m37.583 39.983-1.788-1.788-4.44-4.44m.692 5.802 5.536.426-.425-5.536" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 2. EXCEL-TO-PDF
svgs['excel-to-pdf'] = build_svg('excel-to-pdf',
CONVERTER_CSS_FORWARD.format(prefix='xlp'),
'''<g class="xlp-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="xlp-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#22C55E"/><path d="M11.7 10.8h5.4c.497 0 .9.537.9 1.2v2.4c0 .663-.403 1.2-.9 1.2h-5.4c-.497 0-.9-.537-.9-1.2v-2.4c0-.663.403-1.2.9-1.2zm0 7.2h5.4c.497 0 .9.537.9 1.2v2.4c0 .663-.403 1.2-.9 1.2h-5.4c-.497 0-.9-.537-.9-1.2v-2.4c0-.663.403-1.2.9-1.2zm0 7.2h5.4c.497 0 .9.537.9 1.2v2.4c0 .663-.403 1.2-.9 1.2h-5.4c-.497 0-.9-.537-.9-1.2v-2.4c0-.663.403-1.2.9-1.2zM20.547 12c.455 0 .875.26 1.098.682l2.354 4.451 2.364-4.455c.222-.419.64-.678 1.094-.678.975 0 1.578 1.127 1.077 2.014l-2.893 5.127 2.975 5.226c.509.893-.098 2.033-1.082 2.033-.455 0-.875-.26-1.1-.68L24 21.169l-2.426 4.55a1.26 1.26 0 0 1-1.103.682c-.987 0-1.595-1.143-1.085-2.038l2.972-5.221-2.89-5.121c-.502-.89.102-2.02 1.08-2.02" fill="#ffffff"/></g><g class="xlp-arr"><path d="m37.583 39.983-1.788-1.788-4.44-4.44m.692 5.802 5.536.426-.425-5.536" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 3. POWERPOINT-TO-PDF
svgs['powerpoint-to-pdf'] = build_svg('powerpoint-to-pdf',
CONVERTER_CSS_FORWARD.format(prefix='pp'),
'''<g class="pp-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="pp-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#22C55E"/><path d="M16.414 22.286h2.893q2.2 0 3.785-.765 1.598-.779 2.453-2.163t.855-3.244q0-1.885-.855-3.35-.855-1.476-2.453-2.32-1.584-.844-3.785-.844h-.868C14.883 9.6 12 12.623 12 16.352v10.134c0 1.278.988 2.314 2.207 2.314 1.22 0 2.207-1.036 2.207-2.314zm2.641-3.574c-1.458 0-2.64-1.24-2.64-2.769s1.182-2.77 2.64-2.77h.252q.93 0 1.51.423.578.409.842 1.081.276.672.276 1.464 0 .738-.276 1.332-.264.58-.843.91t-1.51.33z" fill="#ffffff"/></g><g class="pp-arr"><path d="m37.583 39.983-1.788-1.788-4.44-4.44m.692 5.802 5.536.426-.425-5.536" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 4. TXT-TO-PDF
svgs['txt-to-pdf'] = build_svg('txt-to-pdf',
CONVERTER_CSS_FORWARD.format(prefix='tp'),
'''<g class="tp-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="tp-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#22C55E"/><path d="M17.373 14.4c.38 0 .72.236.854.592l.975 2.6.976-2.601a.91.91 0 1 1 1.689.678l-1.498 3.491 1.542 3.557a.918.918 0 1 1-1.701.69l-1.008-2.658-1.007 2.657a.92.92 0 1 1-1.704-.692l1.544-3.554-1.5-3.488a.912.912 0 0 1 .838-1.272m5.305.893c0 .494.4.894.893.894h1.26v6.93a.883.883 0 0 0 1.765 0v-6.93h1.31a.893.893 0 0 0 0-1.787h-4.335c-.493 0-.893.4-.893.893m-13.078 0c0 .494.4.894.893.894h1.26v6.93a.883.883 0 1 0 1.765 0v-6.93h1.31a.893.893 0 0 0 0-1.787h-4.335c-.493 0-.893.4-.893.893" fill="#ffffff"/></g><g class="tp-arr"><path d="m37.583 39.983-1.788-1.788-4.44-4.44m.692 5.802 5.536.426-.425-5.536" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 5. HTML-TO-PDF
svgs['html-to-pdf'] = build_svg('html-to-pdf',
CONVERTER_CSS_FORWARD.format(prefix='hp'),
'''<g class="hp-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="hp-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#22C55E"/><g class="hp-tag"><path d="m28.156 20.6-3.22 2.865c-.234.21-.546.314-.858.314s-.625-.104-.859-.314a1.04 1.04 0 0 1-.35-.769c0-.287.126-.563.35-.769l3.044-2.725-3.044-2.725a1.04 1.04 0 0 1-.35-.77c0-.286.126-.562.35-.768.468-.42 1.249-.42 1.717 0l3.22 2.883c.858.751.858 2.009 0 2.778m-5.834-7.216-3.903 12.23c-.156.489-.644.786-1.17.786-.118 0-.215-.017-.332-.035a1.3 1.3 0 0 1-.425-.192 1.1 1.1 0 0 1-.309-.324.97.97 0 0 1-.106-.83L19.98 12.79c.176-.576.859-.908 1.503-.751s1.034.769.839 1.345m-7.142 8.544a1.017 1.017 0 0 1 0 1.537c-.234.21-.546.314-.858.314-.313 0-.625-.104-.859-.314l-3.22-2.865c-.858-.769-.858-2.01 0-2.778l3.22-2.883c.468-.42 1.249-.42 1.717 0s.468 1.118 0 1.538l-3.044 2.725z" fill="#ffffff"/></g></g><g class="hp-arr"><path d="m37.583 39.983-1.788-1.788-4.44-4.44m.692 5.802 5.536.426-.425-5.536" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 6. IMAGES-TO-PDF
svgs['images-to-pdf'] = build_svg('images-to-pdf',
CONVERTER_CSS_FORWARD.format(prefix='ip'),
'''<g class="ip-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="ip-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#22C55E"/><circle class="ip-sun" cx="15" cy="12.6" r="3" fill="#ffffff"/><path d="M9.6 28.8l6.211-9.6 4.518 6.646 3.953-5.907L28.8 28.8z" fill="#ffffff"/></g><g class="ip-arr"><path d="m37.583 39.983-1.788-1.788-4.44-4.44m.692 5.802 5.536.426-.425-5.536" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 7. PDF-TO-WORD
svgs['pdf-to-word'] = build_svg('pdf-to-word',
CONVERTER_CSS_REVERSE.format(prefix='pw'),
'''<g class="pw-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="pw-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#22C55E"/><path d="M19.753 23.832a1.8 1.8 0 1 1 3.502-.829l1.892 8.39 2.403-7.384a1.404 1.404 0 0 1 2.67 0l2.403 7.383 1.913-8.48a1.681 1.681 0 1 1 3.258.828L34.81 34.28a2.364 2.364 0 0 1-4.474.221l-1.79-4.549-1.8 4.576a2.322 2.322 0 0 1-4.414-.291z" fill="#ffffff"/></g><g class="pw-arr"><path d="m16.392 13.991-1.789-1.788-4.44-4.44m.693 5.803 5.536.425-.426-5.535" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 8. PDF-TO-JPG
svgs['pdf-to-jpg'] = build_svg('pdf-to-jpg',
CONVERTER_CSS_REVERSE.format(prefix='pj'),
'''<g class="pj-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="pj-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#22C55E"/><circle cx="24.6" cy="22.2" r="3" fill="#ffffff"/><path d="m19.2 38.4 6.212-9.6 4.518 6.646 3.953-5.908L38.4 38.4z" fill="#ffffff"/></g><g class="pj-arr"><path d="m16.392 13.991-1.789-1.788-4.44-4.44m.693 5.803 5.536.425-.426-5.535" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 9. PDF-TO-TXT
svgs['pdf-to-txt'] = build_svg('pdf-to-txt',
CONVERTER_CSS_REVERSE.format(prefix='ptt'),
'''<g class="ptt-src"><rect x="7.2" y="4.8" width="24" height="28.8" rx="3.6" fill="#86EFAC"/></g><g class="ptt-target"><rect x="16.8" y="14.4" width="24" height="28.8" rx="3.6" fill="#22C55E"/><path d="M26.974 24c.38 0 .72.236.854.592l.975 2.6.975-2.601a.91.91 0 1 1 1.69.678L29.97 28.76l1.541 3.557a.918.918 0 1 1-1.7.69l-1.008-2.657-1.008 2.656a.92.92 0 1 1-1.703-.692l1.544-3.554-1.5-3.488A.912.912 0 0 1 26.974 24m5.305.893c0 .494.4.894.893.894h1.26v6.93a.883.883 0 0 0 1.765 0v-6.93h1.31a.893.893 0 0 0 0-1.787H33.17c-.492 0-.892.4-.892.893m-13.078 0c0 .494.4.894.894.894h1.26v6.93a.883.883 0 1 0 1.765 0v-6.93h1.31a.893.893 0 0 0 0-1.787h-4.336c-.493 0-.893.4-.893.893" fill="#ffffff"/></g><g class="ptt-arr"><path d="m16.392 13.992-1.789-1.789-4.44-4.44m.693 5.803 5.536.426-.426-5.536" fill="none" stroke="#22C55E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 10. CROP (Blue Group: #3B82F6)
svgs['crop'] = build_svg('crop',
'''.cr-f{animation:cr-frame 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes cr-frame{0%,20%{transform:scale(1) translate(0,0)}25%{transform:scale(0.75) translate(4px,4px)}45%{transform:scale(1.28) translate(-6px,-6px)}65%{transform:scale(0.95)}80%,100%{transform:scale(1)}}''',
'''<path d="M12 4v28a4 4 0 0 0 4 4h28" fill="none" stroke="#3B82F6" stroke-width="3" stroke-linecap="round"/><path d="M36 44V16a4 4 0 0 0-4-4H4" fill="none" stroke="#3B82F6" stroke-width="3" stroke-linecap="round"/><g class="cr-f"><path d="M16 16h16v16H16z" fill="#3B82F6" opacity="0.35"/><path d="M16 16h16v16H16z" fill="none" stroke="#3B82F6" stroke-width="3" stroke-dasharray="4 3"/></g>''')

# 11. METADATA (Purple Group: #8B5CF6 / #C4B5FD)
svgs['metadata'] = build_svg('metadata',
'''.md-info{animation:md-pulse 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes md-pulse{0%,20%{transform:translateY(0) scale(1)}25%{transform:translateY(5px) scale(0.85)}45%{transform:translateY(-14px) scale(1.30)}65%{transform:translateY(-4px) scale(0.95)}80%,100%{transform:translateY(0) scale(1)}}''',
'''<rect x="6" y="8" width="36" height="32" rx="4" fill="none" stroke="#8B5CF6" stroke-width="3"/><path d="M12 16h24M12 24h16M12 32h10" fill="none" stroke="#C4B5FD" stroke-width="3" stroke-linecap="round"/><g class="md-info"><circle cx="34" cy="32" r="8" fill="#8B5CF6"/><path d="M34 28v2m0 4v2" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/></g>''')

# 12. PAINT (Creative Group: #F97316 / #FB923C / #FDBA74 / #FED7AA)
svgs['paint'] = build_svg('paint',
'''.pnt-pal{animation:pnt-sweep 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes pnt-sweep{0%,20%{transform:rotate(0deg) translate(0,0)}25%{transform:rotate(-16deg) translate(-6px,4px) scale(0.9)}45%{transform:rotate(32deg) translate(10px,-8px) scale(1.2)}65%{transform:rotate(-8deg) translate(-3px,2px) scale(0.98)}80%,100%{transform:rotate(0deg) translate(0,0) scale(1)}}''',
'''<g class="pnt-pal"><path d="M24 4C12.95 4 4 12.95 4 24s8.95 20 20 20c2.2 0 4-1.8 4-4 0-1.07-.42-2.03-1.1-2.73-.68-.7-.11-1.27.27-1.27H30c7.73 0 14-6.27 14-14 0-9.94-8.95-18-20-18z" fill="#F97316"/><circle cx="12" cy="20" r="3" fill="#ffffff"/><circle cx="20" cy="12" r="3" fill="#FB923C"/><circle cx="30" cy="14" r="3" fill="#FDBA74"/><circle cx="36" cy="22" r="3" fill="#FED7AA"/></g>''')

# 13. EDIT-PDF (Creative Group: #F97316 / #FB923C / #FED7AA)
svgs['edit-pdf'] = build_svg('edit-pdf',
'''.ep-pen{animation:ep-write 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes ep-write{0%,20%{transform:translate(0,0) rotate(0deg)}25%{transform:translate(-8px,-8px) rotate(-16deg)}45%{transform:translate(16px,12px) rotate(28deg)}65%{transform:translate(4px,3px) rotate(-4deg)}80%,100%{transform:translate(0,0) rotate(0deg)}}''',
'''<rect x="6" y="4" width="36" height="40" rx="4" fill="none" stroke="#F97316" stroke-width="3"/><path d="M12 12h16M12 20h24M12 28h18M12 36h12" fill="none" stroke="#FED7AA" stroke-width="3" stroke-linecap="round"/><g class="ep-pen"><path d="M38.5 6.5l3 3-18 18H20.5v-3l18-18z" fill="#F97316"/><path d="M38.5 6.5l3 3" fill="none" stroke="#FB923C" stroke-width="2" stroke-linecap="round"/></g>''')

# 14. EDIT-TEXT
svgs['edit-text'] = build_svg('edit-text',
'''.et-cursor{animation:et-c 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:14px 24px}
.et-l1{animation:et-line1 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:19px 17.4px}
.et-l2{animation:et-line2 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:19px 24.2px}
.et-l3{animation:et-line3 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:19px 31px}
@keyframes et-c{0%,20%{transform:translate(0,-10px) scale(1)}25%{transform:translate(0,-10px) scale(0.92)}35%{transform:translate(22px,-10px) scale(1.15,0.85)}45%{transform:translate(0,0) scale(1)}55%{transform:translate(18px,0) scale(1.15,0.85)}65%{transform:translate(0,7px) scale(1)}75%{transform:translate(14px,7px) scale(1.1,0.9)}85%,100%{transform:translate(0,-10px) scale(1)}}
@keyframes et-line1{0%,20%{opacity:0;transform:scaleX(0)}35%,80%{opacity:1;transform:scaleX(1)}100%{opacity:0;transform:scaleX(0)}}
@keyframes et-line2{0%,40%{opacity:0;transform:scaleX(0)}55%,80%{opacity:1;transform:scaleX(1)}100%{opacity:0;transform:scaleX(0)}}
@keyframes et-line3{0%,60%{opacity:0;transform:scaleX(0)}75%,80%{opacity:1;transform:scaleX(1)}100%{opacity:0;transform:scaleX(0)}}''',
'''<path class="et-cursor" d="M16.77 38.419V9.58h6.46A2.78 2.78 0 0 0 26 6.791 2.78 2.78 0 0 0 23.23 4H4.77A2.78 2.78 0 0 0 2 6.79a2.78 2.78 0 0 0 2.77 2.791h6.46V38.42H4.77A2.78 2.78 0 0 0 2 41.209 2.78 2.78 0 0 0 4.77 44h18.46A2.78 2.78 0 0 0 26 41.21a2.78 2.78 0 0 0-2.77-2.791z" fill="#F97316"/><path class="et-l1" d="M40.818 15H21.182C19.977 15 19 16.269 19 17.4s.977 2.4 2.182 2.4h19.636c1.205 0 2.182-1.269 2.182-2.4s-.977-2.4-2.182-2.4" fill="#F97316"/><path class="et-l2" d="M36.455 21.8h-15.71c-.963 0-1.745 1.24-1.745 2.4s.782 2.4 1.745 2.4h15.71c.964 0 1.745-1.241 1.745-2.4 0-1.16-.782-2.4-1.745-2.4" fill="#F97316"/><path class="et-l3" d="M31.48 28.6H20.92C19.86 28.6 19 29.8 19 31s.86 2.4 1.92 2.4h10.56c1.06 0 1.92-1.2 1.92-2.4s-.86-2.4-1.92-2.4" fill="#FDBA74"/>''')

# 15. PAGE-NUMBERS
svgs['page-numbers'] = build_svg('page-numbers',
'''.pn-n1{animation:pn-s1 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:8px 24px}
.pn-n2{animation:pn-s2 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
.pn-n3{animation:pn-s3 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:40px 24px}
@keyframes pn-s1{0%,20%{transform:scale(1) translateY(0)}25%{transform:scale(1.35) translateY(-12px)}38%,100%{transform:scale(1) translateY(0)}}
@keyframes pn-s2{0%,32%{transform:scale(1) translateY(0)}37%{transform:scale(1.35) translateY(-12px)}50%,100%{transform:scale(1) translateY(0)}}
@keyframes pn-s3{0%,44%{transform:scale(1) translateY(0)}49%{transform:scale(1.35) translateY(-12px)}62%,100%{transform:scale(1) translateY(0)}}''',
'''<g class="pn-n1"><path d="M5.51 14.451c2.97-.921 5.985 1.293 5.985 4.397v10.766A2.39 2.39 0 0 1 9.104 32a2.39 2.39 0 0 1-2.392-2.386V17.659l-2.6.714a1.666 1.666 0 0 1-.938-3.196z" fill="#3B82F6"/></g><g class="pn-n2"><path d="M27.37 28.633c.846 0 1.532.7 1.532 1.563 0 .864-.686 1.563-1.532 1.563h-9.357c-1.01 0-1.828-.835-1.828-1.866 0-.498.195-.976.542-1.327l5.316-5.368a16 16 0 0 0 1.251-1.527q.476-.686.689-1.238.225-.553.225-.998 0-.758-.238-1.263a1.63 1.63 0 0 0-.676-.781q-.438-.265-1.089-.265-.65 0-1.139.361-.488.361-.763.986c-.308.732-.896 1.407-1.676 1.407h-.702c-1.169 0-2.162-1.003-1.722-2.108q.172-.432.42-.838.826-1.335 2.29-2.128Q20.379 14 22.306 14q2.015 0 3.38.601t2.053 1.744q.7 1.13.7 2.73 0 .913-.3 1.755a7.4 7.4 0 0 1-.864 1.671 14.5 14.5 0 0 1-1.376 1.683 40 40 0 0 1-1.828 1.84l-2.353 2.61z" fill="#3B82F6"/></g><g class="pn-n3"><path d="M37.126 22.309c0-.552.438-.998.978-.998h1.075q.788 0 1.289-.265.513-.276.763-.77.25-.504.25-1.19 0-.528-.237-.974a1.67 1.67 0 0 0-.701-.71q-.476-.276-1.214-.276-.501 0-.977.205-.476.192-.788.553c-.333.4-.717.878-1.231.878h-1.185c-1.168 0-2.188-1.04-1.595-2.067q.145-.252.331-.483.864-1.07 2.266-1.635A8 8 0 0 1 39.19 14q1.94 0 3.404.577 1.465.565 2.279 1.684.825 1.105.826 2.741 0 .902-.439 1.695-.437.794-1.226 1.395-.51.39-1.138.674a5.5 5.5 0 0 1 1.413.709q.814.578 1.252 1.43.438.843.438 1.937 0 1.226-.513 2.188a4.7 4.7 0 0 1-1.44 1.623q-.926.662-2.165 1.01-1.24.337-2.69.337c-.76 0-1.418-.04-2.279-.289C35.9 31.418 35 31 34.5 30.5c-.604-.604-1.177-1.054-1.08-1.903.082-.702.413-1.181 1.059-1.467q.11-.047.24-.075c.503-.108 1.01.088 1.439.371.256.17.557.372.842.574.356.252.774.414 1.165.61.417.208.746.264 1.164.264q.776 0 1.314-.277.55-.288.839-.77.287-.48.287-1.07 0-.89-.312-1.418a1.75 1.75 0 0 0-.89-.77q-.575-.24-1.388-.24h-1.123a.94.94 0 0 1-.93-.95z" fill="#3B82F6"/></g><rect x="2" y="34" width="44" height="6" rx="3" fill="#3B82F6"/>''')

# 16. RENAME
svgs['rename'] = build_svg('rename',
'''.rn-pen{animation:rn-write 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes rn-write{0%,20%{transform:translate(0,0) rotate(0deg)}25%{transform:translate(-10px,-10px) rotate(-14deg)}45%{transform:translate(18px,4px) rotate(26deg)}65%{transform:translate(5px,0) rotate(-4deg)}80%,100%{transform:translate(0,0) rotate(0deg)}}''',
'''<path d="M4 10h16m-8 0v31m-8 0h16" fill="none" stroke="#CBD5E1" stroke-width="3" stroke-linecap="round"/><g class="rn-pen"><path d="M41.768 5.009a3.48 3.48 0 0 0-2.333.686L15.505 27.66c2.281 2.28 3.56 3.559 5.843 5.839L44.304 10.56a3.473 3.473 0 0 0-2.536-5.552" fill="#64748B"/><path d="m13 36 8.348-2.502-5.844-5.839z" fill="#334155"/></g>''')

# 17. SIGN
svgs['sign'] = build_svg('sign',
'''.sg-pen{animation:sg-flourish 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:34px 10px}
@keyframes sg-flourish{0%,20%{transform:translate(0,0) rotate(0deg)}25%{transform:translate(-12px,-10px) rotate(-18deg)}45%{transform:translate(18px,10px) rotate(28deg) scale(1.22)}65%{transform:translate(4px,-2px) rotate(-4deg)}80%,100%{transform:translate(0,0) rotate(0deg)}}''',
'''<g class="sg-pen"><path d="M34.006 5.718a5.86 5.86 0 0 1 6.279-1.315 5.847 5.847 0 0 1 1.998 9.584l-1.146 1.146-14.928 14.928c-1.336 1.33-4.835 2.737-4.835 2.737l-4.54 1.135a2.287 2.287 0 0 1-2.766-2.774l1.132-4.54.034-.123a10.5 10.5 0 0 1 2.706-4.712L32.864 6.86z" fill="#F97316"/></g><path d="M4 43.39c16.214 2.082 25.807-1.257 29.91-8.647 1.36-2.446-1.488-5.903-4.837-1.942-4.46 5.268-1.28 18.146 10.191 4.91-2.264 6.76-.272 6.977 4.736 2.557" fill="none" stroke="#F97316" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>''')

# 18. WATERMARK
svgs['watermark'] = build_svg('watermark',
'''.wm-drop{animation:wm-stamp 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes wm-stamp{0%,20%{transform:translateY(0) scale(1)}25%{transform:translateY(-14px) scale(0.85,1.15)}45%{transform:translateY(8px) scale(1.30,0.70)}65%{transform:translateY(-3px) scale(0.95,1.05)}80%,100%{transform:translateY(0) scale(1)}}''',
'''<g class="wm-drop"><path d="M24.865 4.267a1.092 1.092 0 0 0-1.73 0C18.274 10.688 10 22.055 10 30.457c0 3.55 1.475 6.954 4.1 9.464 2.626 2.51 6.187 3.92 9.9 3.92s7.274-1.41 9.9-3.92c2.625-2.51 4.1-5.914 4.1-9.464 0-8.402-8.273-19.769-13.135-26.19" fill="#F97316"/><path d="M19.692 17.744c1.19 0 2.154-.935 2.154-2.088s-.964-2.088-2.154-2.088-2.154.935-2.154 2.088.965 2.088 2.154 2.088m-4.927 15.013c2.38-.033 1.53-3.297 2.18-5.517.618-2.111 2.885-4.163 1.103-5.516-2-1.52-3.524 2.427-4.228 4.793-.705 2.367-1.596 6.275.945 6.24" fill="#ffffff"/></g><path d="M6 36.842c4.5 4.308 11.25 7 18 7s13.5-2.692 18-7" fill="none" stroke="#FED7AA" stroke-width="3" stroke-linecap="round"/>''')

# 19. CONTINUE-EDIT
svgs['continue-edit'] = build_svg('continue-edit',
'''.ce-pen{animation:ce-draw 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes ce-draw{0%,20%{transform:translate(0,0) rotate(0deg)}25%{transform:translate(-10px,-10px) rotate(-16deg)}45%{transform:translate(18px,18px) rotate(26deg)}65%{transform:translate(4px,4px) rotate(-4deg)}80%,100%{transform:translate(0,0) rotate(0deg)}}''',
'''<g class="ce-pen"><path d="M37.332 2a8.67 8.67 0 0 0-6.129 2.539l-1.074 1.078 12.418 12.09.914-.91A8.669 8.669 0 0 0 37.332 2" fill="#334155"/><path d="m28 8 12.254 12-19.125 19.129c-.191.191-.42.34-.672.441L4.742 45.855a2 2 0 0 1-2.598-2.598L8.43 27.544c.1-.251.25-.48.441-.672z" fill="#64748B"/></g>''')

# 20. DOWNLOAD
svgs['download'] = build_svg('download',
'''.dw-arr{animation:dw-drop 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 20px}
@keyframes dw-drop{0%,20%{transform:translateY(0) scale(1)}25%{transform:translateY(-10px) scale(0.85,1.15)}45%{transform:translateY(18px) scale(1.25,0.75)}65%{transform:translateY(8px) scale(0.95,1.05)}80%,100%{transform:translateY(0) scale(1)}}''',
'''<path d="M6 27v12.467a4.55 4.55 0 0 0 1.318 3.205A4.48 4.48 0 0 0 10.5 44h27a4.48 4.48 0 0 0 3.182-1.328A4.55 4.55 0 0 0 42 39.467V27" fill="none" stroke="#64748B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M34.833 36H13.167C11.97 36 11 37.12 11 38.5s.97 2.5 2.167 2.5h21.666C36.03 41 37 39.88 37 38.5s-.97-2.5-2.167-2.5" fill="#CBD5E1"/><g class="dw-arr"><path d="M20.719 4h6.562c.58 0 1.137.234 1.547.65.41.415.64.979.64 1.567v14.407h4.375a2.18 2.18 0 0 1 1.992 1.373 2.24 2.24 0 0 1-.46 2.395l-9.844 9.974A2.17 2.17 0 0 1 24 35a2.17 2.17 0 0 1-1.531-.634l-9.843-9.974a2.24 2.24 0 0 1-.46-2.396 2.2 2.2 0 0 1 .792-.989 2.17 2.17 0 0 1 1.199-.383h4.375V6.217c0-.588.23-1.152.64-1.568.41-.415.967-.649 1.547-.649" fill="#64748B"/></g>''')

# 21. FLATTEN
svgs['flatten'] = build_svg('flatten',
'''.fl-top{animation:fl-press 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes fl-press{0%,20%{transform:translateY(0) scale(1)}25%{transform:translateY(-12px) scale(1.05)}45%{transform:translateY(14px) scale(1.30,0.65)}65%{transform:translateY(3px) scale(0.95,1.05)}80%,100%{transform:translateY(0) scale(1)}}''',
'''<g class="fl-top"><path d="M40.429 4H7.57C5.6 4 4 4.798 4 6.5S5.599 9 7.571 9H40.43C42.4 9 44 8.202 44 6.5S42.401 4 40.429 4m0 9H7.57C5.6 13 4 13.797 4 15.5S5.599 18 7.571 18H40.43c1.97 0 3.57-.797 3.57-2.5S42.401 13 40.429 13m0 9H7.57C5.6 22 4 22.797 4 24.5S5.599 27 7.571 27H40.43c1.97 0 3.57-.797 3.57-2.5S42.401 22 40.429 22" fill="#C4B5FD"/><path d="M16.5 30v6.5M19 33l-2.5 3.5L14 33m18.5-3v6.5M35 33l-2.5 3.5L30 33" fill="none" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g><path d="M41.222 39H6.778C5.244 39 4 40.755 4 42.5S5.244 46 6.778 46h34.444C42.756 46 44 44.245 44 42.5S42.756 39 41.222 39" fill="#8B5CF6"/>''')

# 22. EXTRACT-PAGES (Blue Group: #3B82F6 / #BFDBFE)
svgs['extract-pages'] = build_svg('extract-pages',
'''.xp-leaf{animation:xp-pull 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes xp-pull{0%,20%{transform:translate(0,0) scale(1)}25%{transform:translate(-5px,-5px) scale(0.9)}45%{transform:translate(14px,-14px) scale(1.22)}65%{transform:translate(3px,-3px) scale(1)}80%,100%{transform:translate(0,0) scale(1)}}''',
'''<rect x="6" y="10" width="28" height="34" rx="3" fill="#BFDBFE"/><g class="xp-leaf"><rect x="14" y="4" width="28" height="34" rx="3" fill="#3B82F6"/><path d="M20 12h16M20 20h16M20 28h10" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/></g>''')

# 23. ORGANIZE (Blue Group: #3B82F6 / #93C5FD)
svgs['organize'] = build_svg('organize',
'''.og-swap{animation:og-flip 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes og-flip{0%,20%{transform:rotate(0deg) scale(1)}25%{transform:rotate(-15deg) scale(0.88)}45%{transform:rotate(180deg) scale(1.22)}65%{transform:rotate(175deg) scale(0.98)}80%,100%{transform:rotate(180deg) scale(1)}}''',
'''<g class="og-swap"><rect x="4" y="8" width="18" height="32" rx="3" fill="#3B82F6"/><rect x="26" y="8" width="18" height="32" rx="3" fill="#93C5FD"/><path d="M10 16h6M10 24h6M32 16h6M32 24h6" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></g>''')

# 24. PROTECT (Protect Group: #EF4444 / #FCA5A5)
svgs['protect'] = build_svg('protect',
'''.pr-shackle{animation:pr-lock 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 16px}
@keyframes pr-lock{0%,20%{transform:translateY(-10px)}25%{transform:translateY(-13px)}45%{transform:translateY(0px)}65%{transform:translateY(-2px)}80%,100%{transform:translateY(-10px)}}''',
'''<g class="pr-shackle"><path d="M14 18V12a10 10 0 0 1 20 0v6" fill="none" stroke="#EF4444" stroke-width="3.5" stroke-linecap="round"/></g><rect x="8" y="18" width="32" height="24" rx="4" fill="#EF4444"/><circle cx="24" cy="28" r="3" fill="#FCA5A5"/><path d="M24 31v4" fill="none" stroke="#FCA5A5" stroke-width="2.5" stroke-linecap="round"/>''')

# 25. DELETE (Delete Group: #64748B / #94A3B8)
svgs['delete'] = build_svg('delete',
'''.del-lid{animation:del-open 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 12px}
@keyframes del-open{0%,20%{transform:rotate(0deg) translateY(0)}25%{transform:rotate(-8deg) translateY(-3px)}45%{transform:rotate(-32deg) translateY(-12px)}65%{transform:rotate(-4deg) translateY(-2px)}80%,100%{transform:rotate(0deg) translateY(0)}}''',
'''<g class="del-lid"><path d="M14 12V8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4M8 12h32" fill="none" stroke="#64748B" stroke-width="3" stroke-linecap="round"/></g><path d="M11 12l2.5 26a3 3 0 0 0 3 2.8h15a3 3 0 0 0 3-2.8l2.5-26" fill="none" stroke="#64748B" stroke-width="3" stroke-linecap="round"/><path d="M19 18v16M24 18v16M29 18v16" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round"/>''')

# 26. REPAIR
svgs['repair'] = build_svg('repair',
'''.rp-key{animation:rp-turn 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes rp-turn{0%,20%{transform:rotate(0deg) scale(1)}25%{transform:rotate(-15deg) scale(0.88)}45%{transform:rotate(60deg) scale(1.25)}65%{transform:rotate(55deg) scale(0.98)}80%,100%{transform:rotate(0deg) scale(1)}}''',
'''<g class="rp-key"><path d="M27 17l10-10a4.24 4.24 0 0 1 6 6L33 23M27 17l-12 12-6-2 2 6-2 2h-4v-4l2-2-2-6 12-12z" fill="none" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 27. MERGE (Blue Group: #3B82F6 / #BFDBFE)
svgs['merge'] = build_svg('merge',
'''.mg-left{animation:mg-l 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:12px 24px}
.mg-right{animation:mg-r 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:36px 24px}
@keyframes mg-l{0%,20%{transform:translateX(0)}25%{transform:translateX(-5px)}45%{transform:translateX(11px)}65%{transform:translateX(2px)}80%,100%{transform:translateX(0)}}
@keyframes mg-r{0%,20%{transform:translateX(0)}25%{transform:translateX(5px)}45%{transform:translateX(-11px)}65%{transform:translateX(-2px)}80%,100%{transform:translateX(0)}}''',
'''<g class="mg-left"><rect x="2" y="8" width="20" height="32" rx="3" fill="#BFDBFE"/><path d="M6 16h12M6 24h12M6 32h8" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round"/></g><g class="mg-right"><rect x="26" y="8" width="20" height="32" rx="3" fill="#3B82F6"/><path d="M30 16h12M30 24h12M30 32h8" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></g>''')

# 28. SPLIT (Blue Group: #3B82F6 / #93C5FD)
svgs['split'] = build_svg('split',
'''.sp-l{animation:sp-left 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:12px 24px}
.sp-r{animation:sp-right 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:36px 24px}
@keyframes sp-left{0%,20%{transform:translateX(0)}25%{transform:translateX(3px)}45%{transform:translateX(-12px)}65%{transform:translateX(-3px)}80%,100%{transform:translateX(0)}}
@keyframes sp-right{0%,20%{transform:translateX(0)}25%{transform:translateX(-3px)}45%{transform:translateX(12px)}65%{transform:translateX(3px)}80%,100%{transform:translateX(0)}}''',
'''<g class="sp-l"><rect x="4" y="8" width="18" height="32" rx="3" fill="#3B82F6"/><path d="M8 16h10M8 24h10M8 32h6" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></g><g class="sp-r"><rect x="26" y="8" width="18" height="32" rx="3" fill="#3B82F6"/><path d="M30 16h10M30 24h10M30 32h6" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/></g><path d="M24 4v40" fill="none" stroke="#93C5FD" stroke-width="2" stroke-dasharray="3 3"/>''')

# 29. UPLOAD (Service Group: #64748B / #94A3B8)
svgs['upload'] = build_svg('upload',
'''.up-arrow{animation:up-fly 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 30px}
@keyframes up-fly{0%,20%{transform:translateY(0) scale(1)}25%{transform:translateY(6px) scale(0.88)}45%{transform:translateY(-15px) scale(1.25)}65%{transform:translateY(-4px) scale(0.95)}80%,100%{transform:translateY(0) scale(1)}}''',
'''<path class="up-cloud" d="M7 36a8.5 8.5 0 0 1 7.2-13.8 11.5 11.5 0 0 1 19.6 0A8.5 8.5 0 0 1 41 36z" fill="#94A3B8"/><g class="up-arrow"><path d="M24 42V18M16 26l8-8 8 8" fill="none" stroke="#64748B" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 30. OCR (Purple Group: #8B5CF6 / #C4B5FD)
svgs['ocr'] = build_svg('ocr',
'''.oc-beam{animation:oc-scan 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes oc-scan{0%,20%{transform:translateY(-14px)}25%{transform:translateY(-16px)}50%{transform:translateY(14px)}65%{transform:translateY(10px)}80%,100%{transform:translateY(-14px)}}''',
'''<rect x="6" y="6" width="36" height="36" rx="4" fill="none" stroke="#8B5CF6" stroke-width="3"/><path d="M12 14h24M12 22h24M12 30h16" fill="none" stroke="#C4B5FD" stroke-width="2.5" stroke-linecap="round"/><g class="oc-beam"><path d="M4 24h40" fill="none" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round"/></g>''')

# 31. ADD-FILE (Service Group: #475569 / #94A3B8)
svgs['add-file'] = build_svg('add-file',
'''.af-p{animation:af-spin 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes af-spin{0%,20%{transform:rotate(0deg) scale(1)}25%{transform:rotate(-20deg) scale(0.85)}45%{transform:rotate(90deg) scale(1.30)}65%{transform:rotate(90deg) scale(0.95)}80%,100%{transform:rotate(0deg) scale(1)}}''',
'''<rect x="6" y="4" width="36" height="40" rx="4" fill="#94A3B8"/><path d="M12 12h24M12 20h16" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/><g class="af-p"><circle cx="32" cy="32" r="10" fill="#475569"/><path d="M32 26v12M26 32h12" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/></g>''')

# 32. COMPARE (Purple Group: #8B5CF6 / #C4B5FD)
svgs['compare'] = build_svg('compare',
'''.cmp-glass{animation:cmp-scan 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:28px 28px}
@keyframes cmp-scan{0%,20%{transform:translate(0,0) rotate(0deg)}25%{transform:translate(-5px,-5px) rotate(-12deg)}45%{transform:translate(12px,-10px) rotate(22deg) scale(1.25)}65%{transform:translate(3px,-2px) rotate(-3deg)}80%,100%{transform:translate(0,0) rotate(0deg)}}''',
'''<rect x="4" y="6" width="18" height="32" rx="3" fill="#C4B5FD"/><rect x="26" y="6" width="18" height="32" rx="3" fill="#8B5CF6"/><g class="cmp-glass"><circle cx="28" cy="24" r="9" fill="none" stroke="#8B5CF6" stroke-width="3"/><path d="M34 30l6 6" fill="none" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round"/></g>''')

# 33. COMPRESS
svgs['compress'] = build_svg('compress',
'''.cp-top{animation:cp-press-t 3s cubic-bezier(0.34,1.4,0.64,1) infinite}
.cp-bot{animation:cp-press-b 3s cubic-bezier(0.34,1.4,0.64,1) infinite}
.cp-mid{animation:cp-squash 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes cp-press-t{0%,20%{transform:translateY(0)}25%{transform:translateY(-5px)}45%{transform:translateY(9px)}65%{transform:translateY(2px)}80%,100%{transform:translateY(0)}}
@keyframes cp-press-b{0%,20%{transform:translateY(0)}25%{transform:translateY(5px)}45%{transform:translateY(-9px)}65%{transform:translateY(-2px)}80%,100%{transform:translateY(0)}}
@keyframes cp-squash{0%,20%{transform:scale(1,1)}25%{transform:scale(0.92,1.08)}45%{transform:scale(1.28,0.50)}65%{transform:scale(0.95,1.08)}80%,100%{transform:scale(1,1)}}''',
'''<g class="cp-top"><path d="M37.714 4H10.286C9.023 4 8 4.895 8 6s1.023 2 2.286 2h27.428C38.977 8 40 7.105 40 6s-1.023-2-2.286-2" fill="#C4B5FD"/><path d="M24 7v8.467m-4-3.2L24 16l4-3.733" fill="none" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g><g class="cp-mid"><path d="M40.667 20H7.333C5.493 20 4 21.343 4 23v2c0 1.657 1.492 3 3.333 3h33.334C42.507 28 44 26.657 44 25v-2c0-1.657-1.492-3-3.333-3" fill="#8B5CF6"/></g><g class="cp-bot"><path d="M37.714 40H10.286C9.023 40 8 40.895 8 42s1.023 2 2.286 2h27.428C38.977 44 40 43.105 40 42s-1.023-2-2.286-2" fill="#C4B5FD"/><path d="M24 41v-9m4 3.733L24 32l-4 3.733" fill="none" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

# 34. DELETE-PAGES (Blue Group: #3B82F6 / #BFDBFE)
svgs['delete-pages'] = build_svg('delete-pages',
'''.dp-del{animation:dp-s 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes dp-s{0%,20%{transform:scale(1) rotate(0deg)}25%{transform:scale(0.85) rotate(-8deg)}45%{transform:scale(1.30) rotate(15deg)}65%{transform:scale(0.95)}80%,100%{transform:scale(1) rotate(0deg)}}''',
'''<rect x="6" y="4" width="36" height="40" rx="4" fill="#BFDBFE"/><g class="dp-del"><circle cx="24" cy="24" r="12" fill="#3B82F6"/><path d="M18 18l12 12M30 18l-12 12" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/></g>''')

# 35. GRAYSCALE
svgs['grayscale'] = build_svg('grayscale',
'''.gs-spin{animation:gs-s 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes gs-s{0%,20%{transform:rotate(0deg) scale(1)}25%{transform:rotate(-20deg) scale(0.88)}45%{transform:rotate(180deg) scale(1.25)}65%{transform:rotate(175deg) scale(0.95)}80%,100%{transform:rotate(180deg) scale(1)}}''',
'''<g class="gs-spin"><circle cx="24" cy="24" r="18" fill="none" stroke="#64748B" stroke-width="3"/><path d="M24 6a18 18 0 0 1 0 36z" fill="#64748B"/></g>''')

# 36. ROTATE (Blue Group: #3B82F6 / #BFDBFE)
svgs['rotate'] = build_svg('rotate',
'''.rt-arr{animation:rt-s 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 24px}
@keyframes rt-s{0%,20%{transform:rotate(0deg) scale(1)}25%{transform:rotate(-20deg) scale(0.88)}45%{transform:rotate(90deg) scale(1.28)}65%{transform:rotate(85deg) scale(0.95)}80%,100%{transform:rotate(90deg) scale(1)}}''',
'''<rect x="10" y="10" width="28" height="28" rx="3" fill="#BFDBFE"/><g class="rt-arr"><path d="M24 4v8M24 4l-4 4M24 4l4 4" fill="none" stroke="#3B82F6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M38 24a14 14 0 1 1-14-14" fill="none" stroke="#3B82F6" stroke-width="3" stroke-linecap="round"/></g>''')

# 37. UNLOCK (Protect Group: #EF4444 / #FCA5A5)
svgs['unlock'] = build_svg('unlock',
'''.ul-shackle{animation:ul-open 3s cubic-bezier(0.34,1.4,0.64,1) infinite;transform-origin:24px 16px}
@keyframes ul-open{0%,20%{transform:translateY(0) rotate(0deg)}25%{transform:translateY(3px) rotate(-5deg)}45%{transform:translateY(-14px) rotate(-24deg)}65%{transform:translateY(-10px) rotate(-20deg)}80%,100%{transform:translateY(0) rotate(0deg)}}''',
'''<g class="ul-shackle"><path d="M14 18V12a10 10 0 0 1 20 0" fill="none" stroke="#EF4444" stroke-width="3.5" stroke-linecap="round"/></g><rect x="8" y="18" width="32" height="24" rx="4" fill="#EF4444"/><circle cx="24" cy="28" r="3" fill="#FCA5A5"/><path d="M24 31v4" fill="none" stroke="#FCA5A5" stroke-width="2.5" stroke-linecap="round"/>''')

print("Defined SVGs count:", len(svgs))
assert len(svgs) == 37, f"Expected 37 SVGs, got {len(svgs)}"

# Replace each SVG in index.html
for slug, new_svg in svgs.items():
    pattern = rf"(slug:\s*[\x27\"]{slug}[\x27\"].*?svg:\s*`)(<svg.*?</svg>)(`)"
    if not re.search(pattern, html, re.DOTALL):
        print(f"ERROR: Could not match slug {slug}")
    html = re.sub(pattern, rf"\1{new_svg}\3", html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated successfully with all 37 custom SVGs!")
