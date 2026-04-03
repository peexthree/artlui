import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix shopping bag link to open side cart if it exists, otherwise go to checkout
# We don't have a side cart in index.html, so it will go to checkout.html
# BUT wait! We should add a side cart to index.html to make the experience consistent.

side_cart_html = """
<!-- Side Cart (SideNavBar) -->
<aside class="fixed right-0 h-full w-80 z-[60] bg-[#FFFFFF] dark:bg-[#1A1C1A] border-l border-[#D0C5AF]/15 flex flex-col p-6 space-y-5 transform translate-x-full lg:translate-x-full transition-transform duration-300">
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
        <a href="checkout.html" class="flex justify-center w-full luxury-gradient text-on-primary py-3.5 rounded-sm font-headline text-[10px] font-bold uppercase tracking-[0.2em] active:translate-x-1 duration-200">
            Proceed to Checkout
        </a>
    </div>
</aside>
"""

# Replace the existing side cart which is currently hardcoded and hidden (lg:hidden) with one that works on all sizes
old_side_cart = r'<!-- Side Cart \(SideNavBar\) -->.*?</aside>'
content = re.sub(old_side_cart, side_cart_html, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
