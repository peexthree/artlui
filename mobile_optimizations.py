import os
import re

files_to_update = ['index.html', 'catalog.html', 'product_detail.html', 'checkout.html', 'order_confirmation.html', 'design_system.html']

mobile_menu_button = """
<button id="mobile-menu-btn" class="md:hidden text-[#1A1C1A] dark:text-[#FAF9F6] focus:outline-none transition-transform active:scale-95 z-50">
    <span class="material-symbols-outlined text-3xl">menu</span>
</button>
"""

mobile_menu_overlay = """
<!-- Mobile Menu Overlay -->
<div id="mobile-menu" class="fixed inset-0 bg-[#FAF9F6] dark:bg-[#1A1C1A] z-[100] transform -translate-x-full transition-transform duration-300 ease-in-out flex flex-col px-6 py-8">
    <div class="flex justify-between items-center mb-12">
        <a href="index.html" class="text-2xl font-bold tracking-tighter text-[#1A1C1A] dark:text-[#FAF9F6] font-headline uppercase">Lui molds</a>
        <button id="close-mobile-menu" class="text-[#1A1C1A] dark:text-[#FAF9F6]">
            <span class="material-symbols-outlined text-3xl">close</span>
        </button>
    </div>
    <div class="flex flex-col space-y-8 font-headline font-light tracking-tight text-xl">
        <a href="catalog.html" class="text-[#735C00] dark:text-[#D4AF37] border-b border-[#D4AF37]/30 pb-2">Catalog</a>
        <a href="catalog.html#new" class="text-[#1A1C1A] dark:text-[#FAF9F6] opacity-80 border-b border-outline/10 pb-2">New Arrivals</a>
        <a href="catalog.html#new" class="text-[#1A1C1A] dark:text-[#FAF9F6] opacity-80 border-b border-outline/10 pb-2">Best Sellers</a>
        <a href="#support" class="text-[#1A1C1A] dark:text-[#FAF9F6] opacity-80 border-b border-outline/10 pb-2">Support/Care</a>
    </div>
    <div class="mt-auto pb-8">
        <div class="flex gap-6">
            <a href="checkout.html" class="flex items-center gap-2 text-[#1A1C1A] dark:text-[#FAF9F6]">
                <span class="material-symbols-outlined">shopping_bag</span>
                <span>Cart</span>
            </a>
            <a href="index.html" class="flex items-center gap-2 text-[#1A1C1A] dark:text-[#FAF9F6]">
                <span class="material-symbols-outlined">person</span>
                <span>Account</span>
            </a>
        </div>
    </div>
</div>
"""

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # Padding and text adjustments
    content = content.replace('px-12', 'px-5 md:px-12')
    content = content.replace('p-12', 'p-6 md:p-12')
    content = content.replace('gap-12', 'gap-8 lg:gap-12')
    content = content.replace('mb-12', 'mb-8 md:mb-12')
    content = content.replace('mt-16', 'mt-10 md:mt-16')
    content = content.replace('py-12', 'py-8 md:py-12')
    content = content.replace('w-80', 'w-full max-w-[320px]') # Make sidecart responsive

    # Inject mobile menu button into nav
    if 'id="mobile-menu-btn"' not in content:
        # Find the div containing the logo and desktop menu.
        # The structure is <div class="flex justify-between ...">
        # Let's insert the hamburger right inside the nav wrapper, before the logo, or right after.
        # Structure is <nav> <div> <logo> <desktop_menu> <cart_icons> </div> </nav>

        # Let's inject it into the cart_icons container so it's on the right
        # Or even better, change the nav structure slightly.
        # Let's insert it inside the flex container at the end if we can find it.
        # But wait, it's easier to just find the cart block and insert after.
        cart_block = r'(<div class="flex items-center space-x-6[^>]*>.*?</div>)'

        # Actually, let's put it next to the cart block
        replacement = r'\1\n' + mobile_menu_button
        content = re.sub(cart_block, replacement, content, flags=re.DOTALL)

    # Inject mobile menu overlay right after <body>
    if 'id="mobile-menu"' not in content:
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + mobile_menu_overlay, content)

    with open(filepath, 'w') as f:
        f.write(content)

print("Mobile optimizations applied.")
