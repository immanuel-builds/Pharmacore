import { fetchProducts, searchProducts, getProductView } from './api.js';
import { ProductCard } from './components/product-card.js';
import { SearchBar } from './components/search-bar.js';

document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    const isProductPage = window.location.pathname.startsWith('/product/');

    if (isProductPage) {
        initProductPage();
    } else {
        initHomePage();
    }
});

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
