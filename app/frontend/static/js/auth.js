async function handleAuth(url, data, errorElementId) {
    const errorElement = document.getElementById(errorElementId);
    errorElement.style.display = 'none';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === 'success') {
            window.location.href = '/';
        } else {
            errorElement.textContent = result.error || 'An error occurred';
            errorElement.style.display = 'block';
        }
    } catch (error) {
        errorElement.textContent = 'Network error';
        errorElement.style.display = 'block';
    }
}

async function logout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST'
        });
        const result = await response.json();
        if (result.status === 'success') {
            window.location.href = '/auth/login';
        }
    } catch (error) {
        console.error('Logout failed', error);
    }
}
