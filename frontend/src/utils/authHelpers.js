// /frontend/src/utils/authHelpers.js
// Utilities for handling token refresh and session restoration

export const refreshToken = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/refresh`, {
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
    const response = await fetch(input, init);
    if (response.status === 401) {
      await refreshToken();
      return await fetch(input, init);
    }
    return response;
  } catch (err) {
    console.error('Fetch with refresh failed:', err);
    throw err;
  }
};
