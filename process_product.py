from bs4 import BeautifulSoup
import re

def process_product():
    with open('/app/product_detail.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # The main CTA button doesn't have text "Add to Cart" directly, it might have icon + text in spans
    # Let's find the large primary buttons
    for btn in soup.find_all('button'):
        if 'bg-primary-container' in btn.get('class', []):
            text = btn.get_text().strip()
            if 'cart' in text.lower() or 'shopping' in text.lower() or 'bag' in text.lower() or 'Add to Bag' in text:
                btn['onclick'] = "addToCart({id: 'mold_1', name: 'Premium Architectural Mold', price: 150}); return false;"
            elif 'Checkout' in text or 'buy' in text.lower():
                btn.name = 'a'
                btn['href'] = 'checkout.html'

    # Make sure we got it, let's just make the first one Add to Cart and the second Checkout if we can't be sure
    ctas = soup.find_all('button', class_=lambda c: c and 'bg-primary-container' in c)
    if ctas:
        ctas[0]['onclick'] = "addToCart({id: 'mold_1', name: 'Premium Architectural Mold', price: 150}); window.location.href='checkout.html'; return false;"

    with open('/app/product_detail.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

process_product()
