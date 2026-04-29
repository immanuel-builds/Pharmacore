export async function fetchProducts() {
    const res = await fetch('/api/catalog/products');
    return res.json();
}

export async function searchProducts(query) {
    const res = await fetch(`/api/catalog/search?q=${encodeURIComponent(query)}`);
    return res.json();
}

export async function getProductView(id) {
    const res = await fetch(`/api/catalog/product-view/${id}`);
    return res.json();
}
