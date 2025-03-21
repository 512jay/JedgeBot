// /frontend/src/api/auth_api.js

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"; // Ensure this is correctly set

// Helper function to handle fetch requests
async function fetchWithCredentials(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        credentials: "include", // Ensures cookies (access & refresh tokens) are included
        headers: {
            "Content-Type": "application/json",
            ...options.headers, // Allow passing additional headers
        },
    });

    if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
    }

    return response.json();
}
// Register request
// Ensure Content-Type is set and body is correctly formatted
export async function register(userData) {
    return fetchWithCredentials(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },  // ✅ Ensure JSON format
        body: JSON.stringify(userData),  // ✅ Convert userData to JSON
    }).catch(error => {
        console.error("Registration failed:", error);
        throw error;  // Pass the error to the frontend UI
    });
}



// /frontend/src/api/auth_api.js

export async function login(email, password) {
    try {
        const response = await fetchWithCredentials(`${API_URL}/auth/login`, {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Login failed with status ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Login error:", error.message);
        throw error;  // Re-throw to allow your UI to display a message
    }
}


// Logout request
export async function logout() {
    return fetchWithCredentials(`${API_URL}/auth/logout`, { method: "POST" });
}

// Check authentication status (used in App.jsx)
export async function checkAuthentication() {
    return fetchWithCredentials(`${API_URL}/auth/check`);
}

// Refresh token (if applicable)
export async function refreshToken() {
    return fetchWithCredentials(`${API_URL}/auth/refresh`, { method: "POST" });
}
