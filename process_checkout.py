import re

with open('checkout.html', 'r') as f:
    content = f.read()

# Replace dummy cart summary with JS rendered one
# The sidebar order summary is contained in:
# <aside class="w-full lg:w-[400px] space-y-8"> ... </aside>
# We can just empty the contents inside the order summary and let JS populate it.
# Actually we can just leave the JS to overwrite the innerHTML of the container.
# In JS, I target: `const orderSummaryContainer = document.querySelector('aside .space-y-8.mb-10');`
# and `const totalsDiv = document.querySelector('aside .space-y-4.pt-8');`
# We should update the "Complete Purchase" button to clear cart and redirect.

old_button = r'<button class="w-full py-6 rounded-md bg-transparent border border-outline text-on-surface font-bold tracking-\[0\.2em\] uppercase text-xs hover:bg-surface-variant active:scale-\[0\.99\] transition-all">'
new_button = r'<button onclick="clearCart(); window.location.href=\'order_confirmation.html\'; return false;" class="w-full py-6 rounded-md bg-transparent border border-outline text-on-surface font-bold tracking-[0.2em] uppercase text-xs hover:bg-surface-variant active:scale-[0.99] transition-all">'

content = re.sub(old_button, new_button, content)

with open('checkout.html', 'w') as f:
    f.write(content)
