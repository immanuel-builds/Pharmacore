export async function fetchProducts() {
    const res = await fetch('/products');
    return res.json();
}

export async function searchProducts(query) {
    const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
    return res.json();
}

export async function getProductView(id) {
    const res = await fetch(`/product-view/${id}`);
    return res.json();
}

export async function getCart() {
    const res = await fetch('/cart');
    return res.json();
}

export async function addToCart(productId, quantity = 1) {
    const res = await fetch('/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity })
    });
    return res.json();
}

export async function removeFromCart(productId) {
    const res = await fetch('/cart/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
    });
    return res.json();
}

export async function createOrder() {
    const res = await fetch('/order/create', { method: 'POST' });
    return res.json();
}

export async function processPayment(orderId) {
    const res = await fetch('/payment/pay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId })
    });
    return res.json();
}
