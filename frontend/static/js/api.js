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
