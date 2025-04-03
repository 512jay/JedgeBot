// /frontend/src/api/api_client.js
// Centralized API client to interact with the backend

const API_URL = import.meta.env.VITE_API_URL;




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
