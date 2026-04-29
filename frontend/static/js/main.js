import { fetchProducts, searchProducts, getProductView, getCart, addToCart, removeFromCart, createOrder, processPayment } from './api.js';
import { ProductCard } from './components/product-card.js';
import { SearchBar } from './components/search-bar.js';

document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    const path = window.location.pathname;

    initGlobalNav();

    if (path.startsWith('/product/')) {
        initProductPage();
    } else if (path === '/shopping-cart') {
        initCartPage();
    } else {
        initHomePage();
    }
});

async function initGlobalNav() {
    const cartData = await getCart();
    const count = cartData.status === 'success' ? cartData.meta.total_items : 0;

    let nav = document.getElementById('global-nav');
    if (!nav) {
        nav = document.createElement('nav');
        nav.id = 'global-nav';
        document.body.prepend(nav);
    }

    nav.innerHTML = `
        <div class="nav-container">
            <a href="/" class="logo">CAT-2</a>
            <a href="/shopping-cart" class="cart-link">
                🛒 Cart (<span id="cart-count">${count}</span>)
            </a>
        </div>
    `;
}

async function updateCartCount() {
    const cartData = await getCart();
    const count = cartData.status === 'success' ? cartData.meta.total_items : 0;
    const counter = document.getElementById('cart-count');
    if (counter) counter.innerText = count;
}

async function initHomePage() {
    const app = document.getElementById('app');
    app.innerHTML = `
        <header>
            <h1>CAT-2 Catalog</h1>
            ${SearchBar()}
        </header>
        <section class="categories-section">
            <div class="category-cards" id="category-cards">
                <div class="category-card" data-category="Pain Relief">🩺 Pain Relief</div>
                <div class="category-card" data-category="Cold & Flu">🤧 Cold & Flu</div>
                <div class="category-card" data-category="Supplements">💊 Supplements</div>
                <div class="category-card" data-category="Antibiotic">🛡️ Antibiotics</div>
            </div>
        </section>
        <main id="product-list" class="grid">
            <div class="loading">Loading products...</div>
        </main>
    `;

    const productList = document.getElementById('product-list');
    const searchInput = document.getElementById('search-input');
    const categoryCards = document.getElementById('category-cards');

    // Category filter logic
    categoryCards.addEventListener('click', (e) => {
        const card = e.target.closest('.category-card');
        if (card) {
            const category = card.dataset.category;
            searchInput.value = category;
            // Trigger search
            searchInput.dispatchEvent(new Event('input'));
        }
    });

    // Initial load
    const data = await fetchProducts();
    renderProducts(data.data);

    // Search logic
    let timeout = null;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(timeout);
        timeout = setTimeout(async () => {
            const query = e.target.value;
            if (!query.trim()) {
                const data = await fetchProducts();
                renderProducts(data.data);
                return;
            }
            productList.innerHTML = '<div class="loading">Searching...</div>';
            const searchData = await searchProducts(query);
            renderProducts(searchData.data);
        }, 300);
    });

    // Delegate click for product view
    productList.addEventListener('click', (e) => {
        const card = e.target.closest('.product-card');
        if (card) {
            const id = card.dataset.id;
            window.location.href = `/product/${id}`;
        }
    });
}

function renderProducts(products) {
    const productList = document.getElementById('product-list');
    if (!products || products.length === 0) {
        productList.innerHTML = '<div class="empty-state">No products found.</div>';
        return;
    }

    productList.innerHTML = products.map(p => ProductCard(p)).join('');

    // Animation
    anime({
        targets: '.product-card',
        opacity: [0, 1],
        translateY: [20, 0],
        delay: anime.stagger(80),
        easing: 'easeOutQuad'
    });
}

async function initProductPage() {
    const app = document.getElementById('app');
    const productId = window.location.pathname.split('/').pop();

    app.innerHTML = '<div class="loading">Fetching product data...</div>';

    const res = await getProductView(productId);
    if (res.status === 'error') {
        app.innerHTML = `<div class="error">${res.error}</div>`;
        return;
    }

    const { product, safety } = res.data;

    app.innerHTML = `
        <div class="product-detail-view">
            <nav><a href="/">← Back to Catalog</a></nav>
            <div class="product-header">
                <h2>${product.name}</h2>
                <p class="generic-name">${product.generic_name}</p>
                <div class="meta-row">
                    <span class="price">₹${product.price}</span>
                    <span class="stock-status ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}">
                        ${product.stock > 0 ? 'In Stock' : 'Out of Stock'}
                    </span>
                    <button id="add-to-cart-btn" class="view-btn" style="width: auto; padding: 0.6rem 2rem;">Add to Cart</button>
                </div>
            </div>

            <div class="content-grid">
                <section class="info-section card">
                    <h3>🧠 Uses</h3>
                    <p>${product.usage}</p>
                </section>

                <section class="info-section card">
                    <h3>⚠️ Warnings</h3>
                    <p>${product.warnings}</p>
                </section>

                <section class="info-section card interaction-block">
                    <h3>💊 Interactions (from CORE)</h3>
                    <div id="safety-data">
                        ${renderSafety(safety)}
                    </div>
                </section>

                <section class="info-section card">
                    <h3>Description</h3>
                    <p>${product.description}</p>
                    <div class="source-info">
                        Confidence: ${product.confidence * 100}% | Source: ${product.source}
                    </div>
                </section>
            </div>
        </div>
    `;

    anime({
        targets: '.card',
        opacity: [0, 1],
        translateX: [-20, 0],
        delay: anime.stagger(100),
        easing: 'easeOutQuad'
    });

    document.getElementById('add-to-cart-btn').addEventListener('click', async () => {
        const res = await addToCart(productId);
        if (res.status === 'success') {
            updateCartCount();
            alert('Added to cart!');
        } else if (res.error === 'Unauthorized') {
             window.location.href = '/dev/login';
        }
    });
}

async function initCartPage() {
    const app = document.getElementById('app');
    app.innerHTML = '<div class="loading">Fetching your cart...</div>';

    const res = await getCart();
    if (res.status === 'error') {
        if (res.error === 'Unauthorized') {
             app.innerHTML = '<div class="error">Please <a href="/dev/login">Login</a> to view your cart.</div>';
        } else {
             app.innerHTML = `<div class="error">${res.error}</div>`;
        }
        return;
    }

    renderCart(res.data);
}

function renderCart(items) {
    const app = document.getElementById('app');
    if (!items || items.length === 0) {
        app.innerHTML = `
            <div class="cart-view">
                <h2>Your Cart</h2>
                <div class="empty-state">Your cart is empty. <a href="/">Go shopping!</a></div>
            </div>
        `;
        return;
    }

    const total = items.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);

    app.innerHTML = `
        <div class="cart-view">
            <h2>Your Cart</h2>
            <div class="cart-items">
                ${items.map(item => `
                    <div class="cart-item card" data-id="${item.product_id}">
                        <div class="item-info">
                            <h3>${item.product.name}</h3>
                            <p>₹${item.product.price} x ${item.quantity}</p>
                        </div>
                        <button class="remove-btn">Remove</button>
                    </div>
                `).join('')}
            </div>
            <div class="cart-summary card">
                <h3>Total: ₹${total}</h3>
                <button id="checkout-btn" class="view-btn">Checkout</button>
            </div>
            <div id="checkout-status" class="checkout-status hidden"></div>
        </div>
    `;

    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const id = e.target.closest('.cart-item').dataset.id;
            await removeFromCart(id);
            initCartPage();
            updateCartCount();
        });
    });

    document.getElementById('checkout-btn').addEventListener('click', handleCheckout);
}

async function handleCheckout() {
    const statusDiv = document.getElementById('checkout-status');
    const checkoutBtn = document.getElementById('checkout-btn');

    statusDiv.classList.remove('hidden');
    statusDiv.innerHTML = '<div class="loading">Creating order and reserving stock...</div>';
    checkoutBtn.disabled = true;

    const orderRes = await createOrder();
    if (orderRes.status === 'error') {
        statusDiv.innerHTML = `<div class="error">${orderRes.error}</div>`;
        checkoutBtn.disabled = false;
        return;
    }

    const { order, ops } = orderRes.data;

    statusDiv.innerHTML = `
        <div class="order-info card">
            <h3>Order #${order.id} Created</h3>
            <p>Estimated Delivery: <strong>${ops.eta_minutes} mins</strong> from ${ops.store_id}</p>
            <p>Total: ₹${order.total_price}</p>
            <button id="pay-btn" class="view-btn">Pay Now</button>
        </div>
    `;

    document.getElementById('pay-btn').addEventListener('click', () => handlePayment(order.id));
}

async function handlePayment(orderId) {
    const statusDiv = document.getElementById('checkout-status');
    statusDiv.innerHTML = '<div class="loading">Processing payment...</div>';

    // Simulate delay for "premium feel"
    setTimeout(async () => {
        const payRes = await processPayment(orderId);
        if (payRes.status === 'success') {
            statusDiv.innerHTML = `
                <div class="success-state card">
                    <h2 style="color: var(--success-color)">✔ Order Confirmed</h2>
                    <p>🚚 Your medicines are on the way! Delivery in 15 mins.</p>
                    <a href="/" class="view-btn" style="text-decoration:none; display:inline-block; text-align:center;">Back to Home</a>
                </div>
            `;
            updateCartCount();
        } else {
            statusDiv.innerHTML = `
                <div class="error-state card">
                    <h2 style="color: var(--error-color)">Payment Failed</h2>
                    <p>Please try again.</p>
                    <button onclick="location.reload()" class="view-btn">Try Again</button>
                </div>
            `;
        }
    }, 2000);
}

function renderSafety(safety) {
    if (!safety.interactions || safety.interactions.length === 0) {
        return '<p class="disclaimer">No known interactions found for this substance alone. Always consult a doctor before combining medications.</p>';
    }

    return safety.interactions.map(i => `
        <div class="interaction-item ${i.severity.toLowerCase()}">
            <strong>${i.severity} Severity:</strong> ${i.description}
            <div class="source-info">Source: ${i.source}</div>
        </div>
    `).join('');
}
