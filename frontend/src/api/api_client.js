// /frontend/src/api/api_client.js
// Centralized API client to interact with the backend
import { config } from "@/config";




// Example: Fetch a message from the backend (general API call)
export const fetchMessage = async () => {
    try {
        return await fetchWithCredentials(`${config.API_URL}/`);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};
// Example: Fetch user profile (general API call)
export const fetchUserProfile = async () => {
    try {
        return await fetchWithCredentials(`${config.API_URL}/profile`);
    } catch (error) {
        console.error("Error fetching user profile:", error);
    }
};
// Example: Fetch user settings (general API call)
