const CART_KEY = 'lui_molds_cart';

function getCart() {
    const cart = localStorage.getItem(CART_KEY);
    return cart ? JSON.parse(cart) : [];
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartUI();
}

function addToCart(product) {
    const cart = getCart();
    const existingItem = cart.find(item => item.id === product.id);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    saveCart(cart);

    // Check if side cart exists and update it, or open it
    const sideCart = document.querySelector('aside.fixed.right-0');
    if (sideCart && sideCart.classList.contains('translate-x-full')) {
        sideCart.classList.remove('translate-x-full');
    }
}

function updateQuantity(productId, newQuantity) {
    let cart = getCart();
    if (newQuantity <= 0) {
        cart = cart.filter(item => item.id !== productId);
    } else {
        const item = cart.find(item => item.id === productId);
        if (item) {
            item.quantity = newQuantity;
        }
    }
    saveCart(cart);
    if (window.location.pathname.includes('checkout')) {
        renderCheckout();
    }
}

function removeFromCart(productId) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== productId);
    saveCart(cart);
    if (window.location.pathname.includes('checkout')) {
        renderCheckout();
    }
}

function clearCart() {
    localStorage.removeItem(CART_KEY);
    updateCartUI();
}

function updateCartUI() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

    // Update all cart counters
    document.querySelectorAll('sup').forEach(el => {
        // Find sup elements that look like cart counters
        if (el.parentElement.textContent.includes('shopping_bag')) {
            el.textContent = totalItems;
        }
    });
    const explicitCounters = document.querySelectorAll('#cart-count');
    explicitCounters.forEach(el => el.textContent = totalItems);

    // Update side carts if they exist
    renderSideCart();
}

function renderSideCart() {
    const sideCarts = document.querySelectorAll('aside.fixed.right-0');
    if (sideCarts.length === 0) return;

    const cart = getCart();
    let subtotal = 0;

    sideCarts.forEach(drawer => {
        // Find the container for items
        const itemsContainer = drawer.querySelector('.flex-grow.space-y-6');
        if (!itemsContainer) return;

        if (cart.length === 0) {
            itemsContainer.innerHTML = '<div class="text-center text-sm text-secondary py-8">Your collection is empty.</div>';
            const subtotalEl = drawer.querySelector('.font-bold:not(.text-[#D4AF37]):not(.text-lg)');
            if(subtotalEl) subtotalEl.textContent = '$0.00';
            return;
        }

        let html = '';
        subtotal = 0;

        cart.forEach(item => {
            subtotal += item.price * item.quantity;
            html += `
            <div class="flex items-center space-x-4">
                <div class="w-14 h-18 bg-surface-container rounded-sm flex items-center justify-center">
                    <span class="material-symbols-outlined opacity-50">category</span>
                </div>
                <div class="flex-grow">
                    <p class="text-xs font-bold font-headline">${item.name}</p>
                    <p class="text-[10px] text-primary font-light">$${item.price.toFixed(2)} x ${item.quantity}</p>
                </div>
                <button onclick="removeFromCart('${item.id}')" class="material-symbols-outlined text-xs opacity-30 hover:opacity-100 transition-opacity">close</button>
            </div>
            `;
        });

        itemsContainer.innerHTML = html;

        // Update subtotal
        // Find element that has subtotal
        const subtotalContainers = drawer.querySelectorAll('.flex.justify-between.mb-4, .flex.justify-between.items-center.font-headline');
        subtotalContainers.forEach(container => {
            const spans = container.querySelectorAll('span');
            if (spans.length >= 2) {
                spans[1].textContent = '$' + subtotal.toFixed(2);
            }
        });
    });
}

function renderCheckout() {
    const cart = getCart();
    const checkoutContainer = document.getElementById('checkout-items-container');
    const totalsContainer = document.getElementById('checkout-totals-container');
    const orderSummaryContainer = document.querySelector('aside .space-y-8.mb-10');

    if (orderSummaryContainer) {
        if (cart.length === 0) {
            orderSummaryContainer.innerHTML = '<p class="text-sm">Your cart is empty.</p>';
        } else {
            let html = '';
            cart.forEach(item => {
                html += `
                <div class="flex items-center space-x-4">
                    <div class="w-20 h-20 rounded-lg overflow-hidden bg-surface-container flex items-center justify-center shrink-0 shadow-sm">
                        <span class="material-symbols-outlined opacity-50">category</span>
                    </div>
                    <div class="flex-1">
                        <h4 class="text-sm font-medium">${item.name}</h4>
                        <div class="flex justify-between items-center mt-2">
                            <span class="text-[10px] font-bold uppercase tracking-widest text-outline">Qty: ${item.quantity}</span>
                            <span class="text-sm font-medium">$${(item.price * item.quantity).toFixed(2)}</span>
                        </div>
                    </div>
                </div>
                `;
            });
            orderSummaryContainer.innerHTML = html;
        }

        // Update totals in checkout sidebar
        let subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        let tax = subtotal * 0.08;
        let total = subtotal + tax;

        const totalsDiv = document.querySelector('aside .space-y-4.pt-8');
        if (totalsDiv) {
            totalsDiv.innerHTML = `
            <div class="flex justify-between text-sm font-light">
                <span class="text-on-surface-variant">Subtotal</span>
                <span>$${subtotal.toFixed(2)}</span>
            </div>
            <div class="flex justify-between text-sm font-light">
                <span class="text-on-surface-variant">Estimated Shipping</span>
                <span class="text-primary">Free</span>
            </div>
            <div class="flex justify-between text-sm font-light">
                <span class="text-on-surface-variant">Tax (8%)</span>
                <span>$${tax.toFixed(2)}</span>
            </div>
            <div class="flex justify-between pt-4 text-xl font-bold border-t border-outline-variant/30 mt-4">
                <span class="tracking-tight">Total</span>
                <span class="text-primary tracking-tight">$${total.toFixed(2)}</span>
            </div>
            `;
        }
    }
}

// Filter logic for catalog
function setupFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const resetBtn = document.getElementById('reset-filters');
    const products = document.querySelectorAll('.product-card');

    if (filterBtns.length === 0 || products.length === 0) return;

    let activeFilters = {
        category: null,
        price: null,
        hardness: null
    };

    function applyFilters() {
        products.forEach(product => {
            let show = true;
            if (activeFilters.category && product.getAttribute('data-category') !== activeFilters.category) show = false;
            if (activeFilters.price && product.getAttribute('data-price') !== activeFilters.price) show = false;
            if (activeFilters.hardness && product.getAttribute('data-hardness') !== activeFilters.hardness) show = false;

            product.style.display = show ? 'block' : 'none';
        });
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-filter-type');
            const value = btn.getAttribute('data-filter-value');

            // Toggle active state on buttons
            document.querySelectorAll(`.filter-btn[data-filter-type="${type}"]`).forEach(b => {
                b.classList.remove('text-primary', 'border-primary', 'font-medium');
                b.classList.add('text-on-background', 'opacity-50', 'border-transparent');
            });

            if (activeFilters[type] === value) {
                // Deselect
                activeFilters[type] = null;
            } else {
                // Select
                activeFilters[type] = value;
                btn.classList.remove('text-on-background', 'opacity-50', 'border-transparent');
                btn.classList.add('text-primary', 'border-primary', 'font-medium');
            }

            applyFilters();
        });
    });

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            activeFilters = { category: null, price: null, hardness: null };
            filterBtns.forEach(b => {
                b.classList.remove('text-primary', 'border-primary', 'font-medium');
                b.classList.add('text-on-background', 'opacity-50', 'border-transparent');
            });
            applyFilters();
        });
    }
}

// Side cart toggle logic
function setupSideCarts() {
    const shoppingBagButtons = document.querySelectorAll('button[data-icon="shopping_bag"], a[href="checkout.html"]');
    const sideCarts = document.querySelectorAll('aside.fixed.right-0');
    const closeButtons = document.querySelectorAll('aside.fixed.right-0 button');

    // Only intercept links to checkout if we have a side cart on this page
    if (sideCarts.length > 0) {
        shoppingBagButtons.forEach(btn => {
            // Check if it's the nav bar link
            if (btn.tagName === 'A') {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    sideCarts.forEach(cart => cart.classList.remove('translate-x-full'));
                });
            } else {
                btn.addEventListener('click', () => {
                    sideCarts.forEach(cart => cart.classList.remove('translate-x-full'));
                });
            }
        });

        closeButtons.forEach(btn => {
            if(btn.textContent.includes('close')) {
                btn.addEventListener('click', () => {
                    sideCarts.forEach(cart => cart.classList.add('translate-x-full'));
                });
            }
        });
    }
}

// Initialize UI on load
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
    setupFilters();
    setupSideCarts();
    if (window.location.pathname.includes('checkout')) {
        renderCheckout();
    }
});


// Preloader logic
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.style.opacity = '0';
        preloader.style.visibility = 'hidden';
        document.body.classList.remove('preloader-active');
        setTimeout(() => {
            preloader.remove();
        }, 600);
    }
});

// Mobile Menu logic
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const closeMobileMenuBtn = document.getElementById('close-mobile-menu');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && closeMobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.remove('-translate-x-full');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        });

        closeMobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.add('-translate-x-full');
            document.body.style.overflow = '';
        });
    }
});
