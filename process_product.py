import re

with open('product_detail.html', 'r') as f:
    content = f.read()

# Fix the Add to Collection button
old_button = r'''<button class="bg-primary-container w-full py-5 rounded-md text-on-primary-container font-headline font-bold tracking-wide shadow-sm hover:opacity-90 active:scale-\[0\.98\] transition-all flex justify-center items-center space-x-3" onclick="addToCart\(\{id: 'mold_1', name: 'Premium Architectural Mold', price: 150\}\); window\.location\.href='checkout\.html'; return false;">'''
new_button = '''<button class="bg-primary-container w-full py-5 rounded-md text-on-primary-container font-headline font-bold tracking-wide shadow-sm hover:opacity-90 active:scale-[0.98] transition-all flex justify-center items-center space-x-3" onclick="addToCart({id: 'petal_texture_plate', name: 'Petal Texture Plate', price: 124.00}); return false;">'''

content = re.sub(old_button, new_button, content)

# Also fix the top nav bar shopping bag to open drawer
old_nav_cart = r'<button class="material-symbols-outlined hover:text-\[#D4AF37\] transition-colors">shopping_bag</button>'
new_nav_cart = r'<button class="material-symbols-outlined hover:text-[#D4AF37] transition-colors" data-icon="shopping_bag">shopping_bag</button>'
content = content.replace(old_nav_cart, new_nav_cart)

# Make sure Proceed to Checkout link is valid
old_checkout = r'<a class="bg-primary-container w-full py-4 rounded-md text-on-primary-container font-headline font-bold text-sm tracking-widest active:translate-x-1 duration-200" href="checkout\.html">\s*Proceed to Checkout\s*</a>'
new_checkout = r'<a class="flex justify-center bg-primary-container w-full py-4 rounded-md text-on-primary-container font-headline font-bold text-sm tracking-widest active:translate-x-1 duration-200" href="checkout.html">\n                    Proceed to Checkout\n                </a>'
content = re.sub(old_checkout, new_checkout, content)

with open('product_detail.html', 'w') as f:
    f.write(content)
