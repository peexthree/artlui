from bs4 import BeautifulSoup

def process_index():
    with open('/app/index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Change title if it exists, otherwise create it
    title = soup.find('title')
    if title:
        title.string = "ArtLui Molds - Home"
    else:
        title = soup.new_tag('title')
        title.string = "ArtLui Molds - Home"
        soup.head.append(title)

    # Remove catalog filters (the div containing buttons like 'Architectural', 'Under $100', etc)
    # The filters are usually in a flex container above the grid. Let's find "Architectural" and remove its parent container
    arch_btn = soup.find(string=lambda t: t and 'Architectural' in t)
    if arch_btn and arch_btn.parent:
        filter_container = arch_btn.parent.find_parent('div', class_=lambda c: c and 'flex' in c)
        if filter_container:
            # Maybe it's a sidebar or a top bar
            # Let's try to remove the whole section that contains filters if it's identifiable, or just the div
            # Actually, looking at tailwind classes from earlier, the filters are in a grid or flex.
            filter_container.decompose()

    # Change heading
    shop_molds = soup.find(string=lambda t: t and 'Shop Molds' in t)
    if shop_molds and shop_molds.parent:
        shop_molds.replace_with("Welcome to ArtLui Molds - Premium Architectural Forms")

    with open('/app/index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

process_index()
