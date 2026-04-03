from bs4 import BeautifulSoup
import sys
import re

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Update navigation links
    for a in soup.find_all('a'):
        href = a.get('href')
        if href == '#':
            text = a.get_text().strip()
            if text == 'Catalog':
                a['href'] = 'catalog.html'
            elif text in ['New Arrivals', 'Best Sellers']:
                a['href'] = 'catalog.html#new'
            elif text == 'Support/Care':
                a['href'] = '#support'
            elif text == 'Home':
                a['href'] = 'index.html'

    # Add an id to header/nav so we can replace them consistently?
    # For now, let's just make the "ArtLui Molds" go to index.html
    for el in soup.find_all(string=re.compile('ArtLui Molds')):
        if el.parent.name == 'div' and 'font-headline' in el.parent.get('class', []):
            new_a = soup.new_tag('a', href='index.html')
            new_a['class'] = el.parent.get('class')
            new_a.string = el.string
            el.parent.replace_with(new_a)

    # Add cart js and update cart links
    # For cart buttons in nav
    for btn in soup.find_all('button'):
        if btn.find('span', string='shopping_bag'):
            btn.name = 'a'
            btn['href'] = 'checkout.html'
            # Add an id to the span so we can update quantity
            span = btn.find('span', string='shopping_bag')
            if not span.find('sup'):
                sup = soup.new_tag('sup', id='cart-count')
                sup['class'] = 'bg-primary text-on-primary rounded-full px-1.5 py-0.5 text-[10px] ml-1'
                sup.string = '0'
                span.append(sup)

        # Link user icon to maybe just home for now
        if btn.find('span', string='person'):
            btn.name = 'a'
            btn['href'] = 'index.html'

    # Save
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Processed {filename}")

import glob
for f in glob.glob('/app/*.html'):
    if 'design_system' not in f:
        process_file(f)
