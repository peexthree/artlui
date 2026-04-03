import re

files = ['catalog.html', 'index.html', 'product_detail.html', 'order_confirmation.html']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # Need to make sure the main menu shopping cart icon is triggering the side cart, and has the correct counter
    if file != 'checkout.html':
        old_nav_cart = r'<button class="material-symbols-outlined hover:text-\[#D4AF37\] transition-colors">shopping_bag</button>'
        new_nav_cart = r'<button class="material-symbols-outlined hover:text-[#D4AF37] transition-colors" data-icon="shopping_bag">shopping_bag<sup class="bg-primary text-on-primary rounded-full px-1.5 py-0.5 text-[10px] ml-1" id="cart-count">0</sup></button>'
        content = content.replace(old_nav_cart, new_nav_cart)

        # Another pattern
        old_nav_cart2 = r'<button class="material-symbols-outlined hover:scale-110 transition-transform" data-icon="shopping_bag">shopping_bag</button>'
        new_nav_cart2 = r'<button class="material-symbols-outlined hover:scale-110 transition-transform" data-icon="shopping_bag">shopping_bag<sup class="bg-primary text-on-primary rounded-full px-1.5 py-0.5 text-[10px] ml-1" id="cart-count">0</sup></button>'
        content = content.replace(old_nav_cart2, new_nav_cart2)

        # Another pattern
        old_nav_cart3 = r'<button class="material-symbols-outlined hover:text-\[#D4AF37\] transition-colors" data-icon="shopping_bag">shopping_bag</button>'
        new_nav_cart3 = r'<button class="material-symbols-outlined hover:text-[#D4AF37] transition-colors" data-icon="shopping_bag">shopping_bag<sup class="bg-primary text-on-primary rounded-full px-1.5 py-0.5 text-[10px] ml-1" id="cart-count">0</sup></button>'
        content = content.replace(old_nav_cart3, new_nav_cart3)

    with open(file, 'w') as f:
        f.write(content)
