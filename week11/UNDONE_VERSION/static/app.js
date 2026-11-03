document.addEventListener('DOMContentLoaded', () => {
    fetchHealth();
    fetchCacheData();
    fetchCacheStatus();

    // Forms
    document.getElementById('user-form').addEventListener('submit', createUser);
    document.getElementById('find-user-form').addEventListener('submit', findUser);
    document.getElementById('product-form').addEventListener('submit', createProduct);
    document.getElementById('find-product-form').addEventListener('submit', findProduct);
    document.getElementById('refresh-btn').addEventListener('click', removeCache);
});

async function findUser(e) {
    e.preventDefault();
    const id = document.getElementById('find-user-id').value;
    const resultDiv = document.getElementById('find-user-result');
    resultDiv.innerHTML = 'Searching...';

    try {
        const res = await fetch(`/users/${id}`);
        const data = await res.json();
        
        if (res.ok) {
            resultDiv.innerHTML = `
                <div class="result-box success">
                    <p><strong>ID:</strong> ${data.id}</p>
                    <p><strong>Username:</strong> ${data.username}</p>
                    <p><strong>Email:</strong> ${data.email}</p>
                    <p><strong>Role:</strong> ${data.role}</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<div class="result-box error">${data.error}</div>`;
        }
    } catch (err) {
        resultDiv.innerHTML = `<div class="result-box error">Failed to fetch user</div>`;
    }
}

async function findProduct(e) {
    e.preventDefault();
    const id = document.getElementById('find-prod-id').value;
    const resultDiv = document.getElementById('find-product-result');
    resultDiv.innerHTML = 'Searching...';

    try {
        const res = await fetch(`/products/${id}`);
        const data = await res.json();
        
        if (res.ok) {
            resultDiv.innerHTML = `
                <div class="result-box success">
                    <p><strong>ID:</strong> ${data._id}</p>
                    <p><strong>Name:</strong> ${data.name}</p>
                    <p><strong>Price:</strong> $${data.price}</p>
                    <p><strong>Category:</strong> ${data.category || 'N/A'}</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<div class="result-box error">${data.error}</div>`;
        }
    } catch (err) {
        resultDiv.innerHTML = `<div class="result-box error">Failed to fetch product</div>`;
    }
}

async function fetchHealth() {
    try {
        const res = await fetch('/health');
        const data = await res.json();
        updateStatus('mysql', data.mysql);
        updateStatus('mongo', data.mongo);
        updateStatus('redis', data.redis);
    } catch (e) {
        console.error("Health check failed", e);
    }
}

function updateStatus(id, status) {
    const el = document.getElementById(`${id}-status`);
    if (status === 'up') {
        el.classList.add('up');
        el.classList.remove('down');
    } else {
        el.classList.add('down');
        el.classList.remove('up');
    }
}

async function createUser(e) {
    e.preventDefault();
    const data = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        role: document.getElementById('role').value
    };

    try {
        const res = await fetch('/users', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await res.json();
        if (res.ok) {
            alert(`User created! ID: ${result.id}`);
            document.getElementById('user-form').reset();
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (err) {
        alert("Failed to create user");
    }
}

async function createProduct(e) {
    e.preventDefault();
    const data = {
        _id: document.getElementById('prod-id').value,
        name: document.getElementById('prod-name').value,
        price: parseInt(document.getElementById('prod-price').value),
        category: "General" // Default for now
    };

    try {
        const res = await fetch('/products', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await res.json();
        if (res.ok) {
            alert("Product added!");
            document.getElementById('product-form').reset();
            fetchCacheData(); // Refresh explorer
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (err) {
        alert("Failed to add product");
    }
}

async function fetchCacheData() {
    const list = document.getElementById('product-list');
    list.innerHTML = '<p>Loading cache...</p>';
    
    try {
        const res = await fetch('/cache/all');
        const cache = await res.json();
        
        list.innerHTML = '';
        const keys = Object.keys(cache);
        
        if (keys.length === 0) {
            list.innerHTML = '<p class="empty-msg">No data in cache.</p>';
            return;
        }

        keys.forEach(key => {
            const item = document.createElement('div');
            item.className = 'cache-item';
            const val = cache[key];
            const displayVal = typeof val === 'object' ? JSON.stringify(val, null, 2) : val;
            
            item.innerHTML = `
                <div class="cache-header">
                    <span class="cache-key">${key}</span>
                </div>
                <pre class="cache-value">${displayVal}</pre>
            `;
            list.appendChild(item);
        });
        
        fetchCacheStatus();
    } catch (err) {
        list.innerHTML = '<p>Error loading cache explorer.</p>';
    }
}

async function removeCache() {
    try {
        const res = await fetch('/cache/remove', { method: 'POST' });
        const data = await res.json();
        alert(data.message || data.error);
        fetchCacheStatus();
    } catch (err) {
        alert("Cache removal failed");
    }
}

async function fetchCacheStatus() {
    try {
        const res = await fetch('/cache/status');
        const data = await res.json();
        document.getElementById('key-count').innerText = data.total_cached_keys || 0;
    } catch (err) {
        console.error("Cache status check failed");
    }
}
