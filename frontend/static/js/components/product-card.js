export function ProductCard(product) {
    return `
        <div class="product-card" data-id="${product.id}">
            <div class="product-info">
                <h3>${product.name}</h3>
                <p class="generic-name">${product.generic_name}</p>
                <p class="category-tag">${product.category}</p>
            </div>
            <div class="product-meta">
                <span class="price">₹${product.price}</span>
                <span class="stock-status ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}">
                    ${product.stock > 0 ? 'In Stock' : 'Out of Stock'}
                </span>
            </div>
            <button class="view-btn">View Details</button>
        </div>
    `;
}
