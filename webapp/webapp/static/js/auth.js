// API Communication Functions
const login = async (credentials) => {
    const response = await fetch('/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
    });
    if (!response.ok) throw new Error('Login failed');
    return await response.json();
};

const register = async (userData) => {
    const response = await fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    if (!response.ok) throw new Error('Registration failed');
    return await response.json();
};

const fetchProtectedData = async (endpoint) => {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('No access token');
    
    const response = await fetch(endpoint, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) throw new Error('Request failed');
    return await response.json();
};