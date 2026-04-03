import re

with open('catalog.html', 'r') as f:
    content = f.read()

# Add a specific ID to the filter buttons for easier JS targeting, or update existing ones
# Add data-category, data-price, data-hardness attributes to the products
# Let's replace the product cards to include data attributes and Add to Cart buttons.

products_data = [
    {
        'id': 'fluted_column',
        'name': 'The Fluted Column',
        'price': 124.00,
        'category': 'Architectural',
        'hardness': '25A',
        'price_range': '100-200'
    },
    {
        'id': 'lichen_basin',
        'name': 'Lichen Basin',
        'price': 189.00,
        'category': 'Organic Forms',
        'hardness': '15A',
        'price_range': '100-200'
    },
    {
        'id': 'prism_totem',
        'name': 'Prism Totem',
        'price': 95.00,
        'category': 'Geometric Series',
        'hardness': '40A',
        'price_range': 'under-100'
    },
    {
        'id': 'the_monolith',
        'name': 'The Monolith',
        'price': 210.00,
        'category': 'Architectural',
        'hardness': '40A',
        'price_range': 'over-200'
    },
    {
        'id': 'doric_pillar',
        'name': 'Doric Pillar',
        'price': 155.00,
        'category': 'Architectural',
        'hardness': '25A',
        'price_range': '100-200'
    },
    {
        'id': 'aqueous_curve',
        'name': 'Aqueous Curve',
        'price': 78.00,
        'category': 'Organic Forms',
        'hardness': '15A',
        'price_range': 'under-100'
    }
]

# We need to insert these data attributes into the product card div and modify the button
import re
products = re.split(r'<!-- Product Card \d+ -->', content)

new_content = products[0]

for i in range(1, len(products)):
    product_chunk = products[i]
    if i <= len(products_data):
        data = products_data[i-1]

        # Add data attributes to the main group div
        product_chunk = product_chunk.replace('<div class="group">',
            f'<div class="group product-card" data-category="{data["category"]}" data-price="{data["price_range"]}" data-hardness="{data["hardness"]}">')

        # Change Quick View link to Add to Cart button
        add_to_cart_btn = f'''<button onclick="addToCart({{id: '{data['id']}', name: '{data['name']}', price: {data['price']}}}); return false;" class="luxury-gradient text-on-primary px-6 py-2.5 rounded-sm font-label text-[10px] font-bold uppercase tracking-widest transform translate-y-2 group-hover:translate-y-0 transition-all duration-500">Add to Cart</button>'''

        # Replace the a tag and button inside it
        product_chunk = re.sub(r'<a href="product_detail\.html">\s*<div class="absolute inset-0[^>]*>\s*<button[^>]*>Quick View</button>\s*</div>\s*</a>',
            f'<div class="absolute inset-0 bg-on-background/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex items-center justify-center space-x-2">\n<a href="product_detail.html" class="bg-surface text-on-surface px-6 py-2.5 rounded-sm font-label text-[10px] font-bold uppercase tracking-widest transform translate-y-2 group-hover:translate-y-0 transition-all duration-500">View</a>\n{add_to_cart_btn}\n</div>',
            product_chunk)

    new_content += f'<!-- Product Card {i} -->' + product_chunk

# Update filters
filter_mapping = [
    # Categories
    (r'<button class="font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5">Architectural</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="category" data-filter-value="Architectural">Architectural</button>'),
    (r'<button class="font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5">Organic Forms</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="category" data-filter-value="Organic Forms">Organic Forms</button>'),
    (r'<button class="font-body text-xs text-primary border-b border-primary pb-0.5 font-medium">Geometric Series</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="category" data-filter-value="Geometric Series">Geometric Series</button>'),

    # Price
    (r'<button class="font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5">Under \$100</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="price" data-filter-value="under-100">Under $100</button>'),
    (r'<button class="font-body text-xs text-primary border-b border-primary pb-0.5 font-medium">\$100 - \$200</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="price" data-filter-value="100-200">$100 - $200</button>'),
    (r'<button class="font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5">Over \$200</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="price" data-filter-value="over-200">Over $200</button>'),

    # Hardness
    (r'<button class="font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5">Soft \(15A\)</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="hardness" data-filter-value="15A">Soft (15A)</button>'),
    (r'<button class="font-body text-xs text-primary border-b border-primary pb-0.5 font-medium">Mid \(25A\)</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="hardness" data-filter-value="25A">Mid (25A)</button>'),
    (r'<button class="font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5">Firm \(40A\)</button>',
     r'<button class="filter-btn font-body text-xs text-on-background opacity-50 hover:opacity-100 transition-opacity border-b border-transparent hover:border-on-background pb-0.5" data-filter-type="hardness" data-filter-value="40A">Firm (40A)</button>'),

    # Reset
    (r'<button class="text-\[10px\] font-bold uppercase tracking-tighter text-primary/60 hover:text-primary transition-colors underline underline-offset-4">Reset all filters</button>',
     r'<button id="reset-filters" class="text-[10px] font-bold uppercase tracking-tighter text-primary/60 hover:text-primary transition-colors underline underline-offset-4">Reset all filters</button>')
]

for old, new in filter_mapping:
    new_content = re.sub(old, new, new_content)

with open('catalog.html', 'w') as f:
    f.write(new_content)
