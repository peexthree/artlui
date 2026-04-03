const CART_KEY = 'artlui_cart';

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
    alert('Added to cart!');
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

function clearCart() {
    localStorage.removeItem(CART_KEY);
    updateCartUI();
}

function updateCartUI() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

    // Update all cart counters
    document.querySelectorAll('#cart-count').forEach(el => {
        el.textContent = totalItems;
        // Optionally show/hide based on count
        // el.style.display = totalItems > 0 ? 'inline' : 'none';
    });
}

function renderCheckout() {
    const cart = getCart();
    const checkoutContainer = document.getElementById('checkout-items-container');
    const totalsContainer = document.getElementById('checkout-totals-container');

    if (!checkoutContainer || !totalsContainer) return;

    if (cart.length === 0) {
        checkoutContainer.innerHTML = '<p>Your cart is empty.</p>';
        totalsContainer.innerHTML = '';
        return;
    }

    let html = '';
    let subtotal = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        html += `
            <div class="flex items-center gap-4 py-4 border-b border-outline/20">
                <div class="w-16 h-16 bg-surface-variant flex items-center justify-center rounded">
                    <span class="material-symbols-outlined opacity-50">image</span>
                </div>
                <div class="flex-1">
                    <h3 class="text-sm font-medium text-on-surface">${item.name}</h3>
                    <p class="text-xs text-on-surface/70">$${item.price.toFixed(2)}</p>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="updateQuantity('${item.id}', ${item.quantity - 1})" class="w-6 h-6 rounded bg-surface-variant flex items-center justify-center">-</button>
                    <span class="text-sm">${item.quantity}</span>
                    <button type="button" onclick="updateQuantity('${item.id}', ${item.quantity + 1})" class="w-6 h-6 rounded bg-surface-variant flex items-center justify-center">+</button>
                </div>
                <div class="text-sm font-medium ml-4">$${itemTotal.toFixed(2)}</div>
            </div>
        `;
    });

    checkoutContainer.innerHTML = html;

    const tax = subtotal * 0.08; // 8% tax
    const shipping = 15.00;
    const total = subtotal + tax + shipping;

    totalsContainer.innerHTML = `
        <div class="space-y-2 text-sm">
            <div class="flex justify-between">
                <span class="text-on-surface/70">Subtotal</span>
                <span>$${subtotal.toFixed(2)}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-on-surface/70">Shipping</span>
                <span>$${shipping.toFixed(2)}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-on-surface/70">Tax</span>
                <span>$${tax.toFixed(2)}</span>
            </div>
            <div class="flex justify-between font-bold text-lg pt-4 border-t border-outline/20 mt-4">
                <span>Total</span>
                <span>$${total.toFixed(2)}</span>
            </div>
        </div>
    `;
}

// Initialize UI on load
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
    if (window.location.pathname.includes('checkout')) {
        renderCheckout();
    }
});
