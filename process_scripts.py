import glob
from bs4 import BeautifulSoup
import re
import uuid

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 1. Inject script
    if not soup.find('script', src='src/js/main.js'):
        script = soup.new_tag('script', src='src/js/main.js')
        if soup.body:
            soup.body.append(script)

    # 2. Update catalog "Quick View" and products
    if 'catalog.html' in filename or 'index.html' in filename:
        for btn in soup.find_all('button', string=re.compile('Quick View', re.I)):
            # Create link to product_detail.html
            parent_a = soup.new_tag('a', href='product_detail.html')
            btn.parent.insert_before(parent_a)
            parent_a.append(btn.parent.extract())

    # 3. Update Product Detail "Add to Cart"
    if 'product_detail.html' in filename:
        # Find Add to Cart button
        for btn in soup.find_all('button', string=re.compile('Add to Cart', re.I)):
            btn['onclick'] = "addToCart({id: 'mold_1', name: 'Premium Architectural Mold', price: 150}); return false;"
        for btn in soup.find_all('button', string=re.compile('Buy Now', re.I)):
            btn.name = 'a'
            btn['href'] = 'checkout.html'

    # 4. Update checkout.html to have containers
    if 'checkout.html' in filename:
        # We need to find where the order summary is and inject the containers
        # The summary is usually on the right side.
        # Let's look for "Order Summary"
        summary_h2 = soup.find(string=re.compile('Order Summary', re.I))
        if summary_h2 and summary_h2.parent:
            container_div = summary_h2.parent.parent
            # Clear contents after the header
            for el in container_div.find_all(recursive=False):
                if el != summary_h2.parent and el.name != 'button': # keep header and place order btn
                    el.decompose()

            # Insert our containers
            items_container = soup.new_tag('div', id='checkout-items-container')
            items_container['class'] = 'mb-6'

            totals_container = soup.new_tag('div', id='checkout-totals-container')

            summary_h2.parent.insert_after(items_container)
            items_container.insert_after(totals_container)

        # Update Form action and Place Order button
        form = soup.find('form')
        if form:
            form['action'] = 'order_confirmation.html'
            form['onsubmit'] = "clearCart(); return true;"
        else:
            # Maybe place order is a button
            for btn in soup.find_all('button', string=re.compile('Place Order', re.I)):
                btn.name = 'a'
                btn['href'] = 'order_confirmation.html'
                btn['onclick'] = "clearCart();"

    # 5. Order confirmation
    if 'order_confirmation.html' in filename:
        for a in soup.find_all('a', string=re.compile('Continue Shopping', re.I)):
            a['href'] = 'catalog.html'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Processed {filename}")

for f in glob.glob('/app/*.html'):
    if 'design_system' not in f:
        process_file(f)
