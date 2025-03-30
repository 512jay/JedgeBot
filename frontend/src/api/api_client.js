// /frontend/src/api/api_client.js
// Centralized API client to interact with the backend

const API_URL = import.meta.env.VITE_API_URL;

export async function fetchWithCredentials(url, options = {}) {
  const res = await fetch(url, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    let error = new Error(`HTTP Error: ${res.status}`);
    error.status = res.status;

    try {
      const data = await res.json();
      error.detail = data.detail || null;
    } catch {
      // non-JSON error, ignore
    }

    throw error;
  }

  return res;
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
    