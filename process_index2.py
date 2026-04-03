from bs4 import BeautifulSoup

def fix_heading():
    with open('/app/index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Try to find the main heading (likely an h1 or something looking like a title)
    h1 = soup.find('h1')
    if h1:
        h1.string = "Welcome to ArtLui Molds - Premium Architectural Forms"
    else:
        # Look for text that might be the title
        for el in soup.find_all(['h2', 'div', 'p']):
            if el.string and ('molds' in el.string.lower() or 'catalog' in el.string.lower()):
                if 'class' in el.attrs and ('text-3xl' in el['class'] or 'text-4xl' in el['class']):
                    el.string = "Welcome to ArtLui Molds - Premium Architectural Forms"
                    break

    with open('/app/index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

fix_heading()
