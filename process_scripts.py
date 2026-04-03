import re

files = ['catalog.html', 'index.html', 'checkout.html', 'order_confirmation.html', 'product_detail.html']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Update product_detail to ensure proper side cart
    if file == 'product_detail.html':
        side_cart_html = """
<!-- Side Cart (SideNavBar) -->
<aside class="fixed right-0 h-full w-80 z-[60] bg-[#FFFFFF] dark:bg-[#1A1C1A] border-l border-[#D0C5AF]/15 flex flex-col p-6 space-y-5 transform translate-x-full transition-transform duration-300">
    <div class="flex justify-between items-start">
        <div>
            <h2 class="text-base font-bold text-[#D4AF37] font-headline uppercase tracking-wider">Your Selection</h2>
            <p class="font-body text-[10px] opacity-60">Artisanal Mold Collection</p>
        </div>
        <button class="material-symbols-outlined text-xl">close</button>
    </div>
    <div class="flex-grow space-y-6 py-6 overflow-y-auto">
        <!-- JS populated items -->
    </div>
    <div class="pt-6 border-t border-outline-variant/15">
        <div class="flex justify-between mb-4 font-headline text-xs">
            <span>Subtotal</span>
            <span class="font-bold">$0.00</span>
        </div>
        <a href="checkout.html" class="flex justify-center w-full bg-primary-container text-on-primary-container py-3.5 rounded-sm font-headline text-[10px] font-bold uppercase tracking-[0.2em] active:translate-x-1 duration-200">
            Proceed to Checkout
        </a>
    </div>
</aside>
"""
        old_side_cart = r'<!-- SideNavBar \(Hidden Cart Trigger\) -->.*?</aside>'
        content = re.sub(old_side_cart, side_cart_html, content, flags=re.DOTALL)

    # Update script tag correctly
    if '<script src="src/js/main.js"></script>' not in content:
        content = content.replace('</body>', '<script src="src/js/main.js"></script></body>')

    with open(file, 'w') as f:
        f.write(content)
