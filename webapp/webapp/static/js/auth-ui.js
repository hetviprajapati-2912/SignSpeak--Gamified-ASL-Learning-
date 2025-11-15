// UI Handling Functions
function showLoginModal() {
    document.getElementById('loginModal').classList.remove('hidden');
}

function hideLoginModal() {
    document.getElementById('loginModal').classList.add('hidden');
}

async function performLogin() {
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    if (!username || !password) {
        showAlert('Please enter both username and password', 'error');
        return;
    }

    try {
        const loginBtn = document.getElementById('loginSubmitBtn');
        loginBtn.disabled = true;
        loginBtn.innerHTML = '<span class="spinner">Loading...</span>';

        const response = await login({ username, password });

        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        
        hideLoginModal();
        updateAuthUI();
        showAlert('Login successful!', 'success');
    } catch (error) {
        console.error("Login failed:", error);
        showAlert('Login failed. Please check your credentials.', 'error');
    } finally {
        const loginBtn = document.getElementById('loginSubmitBtn');
        if (loginBtn) {
            loginBtn.disabled = false;
            loginBtn.textContent = 'Sign In';
        }
    }
}

function updateAuthUI() {
    const token = localStorage.getItem('access_token');
    const loginBtn = document.querySelector('[data-auth-button]');
    
    if (!loginBtn) return;

    if (token) {
        loginBtn.textContent = "Logout";
        loginBtn.onclick = handleLogout;
        loginBtn.classList.remove('text-purple-600');
        loginBtn.classList.add('text-red-600');
    } else {
        loginBtn.textContent = "Login";
        loginBtn.onclick = showLoginModal;
        loginBtn.classList.remove('text-red-600');
        loginBtn.classList.add('text-purple-600');
    }
}

function handleLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    updateAuthUI();
    showAlert('Logged out successfully', 'success');
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg ${
        type === 'error' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
    }`;
    alertDiv.textContent = message;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.classList.add('opacity-0', 'transition-opacity', 'duration-300');
        setTimeout(() => alertDiv.remove(), 300);
    }, 3000);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    
    // Close modal when clicking outside
    document.getElementById('loginModal')?.addEventListener('click', (e) => {
        if (e.target === document.getElementById('loginModal')) {
            hideLoginModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !document.getElementById('loginModal').classList.contains('hidden')) {
            hideLoginModal();
        }
    });
});