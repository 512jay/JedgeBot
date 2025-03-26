// /frontend/src/utils/authHelpers.js
// Utilities for handling token refresh and session restoration

const BASE_URL = import.meta.env.VITE_API_URL;

export const refreshToken = async () => {
  try {
    const response = await fetch(`${BASE_URL}/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error refreshing token:", error);
    throw error;
  }
};

export const fetchWithRefresh = async (input, init = {}) => {
  try {
    let response = await fetch(input, init);

    if (response.status === 401) {
      const refreshed = await refreshToken();
      if (refreshed) {
        response = await fetch(input, init);
      }
    }

    return response;
  } catch (err) {
    console.error('Fetch with refresh failed:', err);
    throw err;
  }
};
