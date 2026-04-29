export const api = {
    async get(url) {
        const res = await fetch(url);
        return res.json();
    },
    async post(url, data) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    }
};

export const state = {
    user: null,
    cart: [],
    settings: {
        animations: localStorage.getItem('animations') !== 'false'
    }
};

export function animatePageIn(selector = '#app-root') {
    if (!state.settings.animations) return;
    anime({
        targets: selector,
        opacity: [0, 1],
        translateY: [20, 0],
        duration: 800,
        easing: 'easeOutQuad'
    });
}
