// /frontend/src/api/api_client.js
// Centralized API client to interact with the backend

const API_URL = import.meta.env.VITE_API_URL;

// General function to handle API requests with authentication cookies
export async function fetchWithCredentials(url, options = {}) {
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

// Example: Fetch a message from the backend (general API call)
export const fetchMessage = async () => {
    try {
        return await fetchWithCredentials(`${API_URL}/`);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};
// Example: Fetch user profile (general API call)
export const fetchUserProfile = async () => {
    try {
        return await fetchWithCredentials(`${API_URL}/profile`);
    } catch (error) {
        console.error("Error fetching user profile:", error);
    }
};
// Example: Fetch user settings (general API call)  
    