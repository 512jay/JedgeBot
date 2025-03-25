// /frontend/src/utils/authHelpers.js
// Utilities for handling token refresh and session restoration
const BASE_URL = import.meta.env?.VITE_API_URL || "http://localhost:8000";

export async function fetchWithRefresh(url, options = {}) {
  try {
    const response = await fetch(url.startsWith("http") ? url : `${BASE_URL}${url}`, { ... });

      ...options,
      credentials: 'include', // Send cookies
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
    });

    // If not authorized, try refreshing token
    if (response.status === 401) {
      const refreshResponse = await fetch('/auth/refresh', {
        method: 'POST',
        credentials: 'include',
      });

      if (refreshResponse.ok) {
        // Retry original request after successful refresh
        const retry = await fetch(url, {
          ...options,
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {}),
          },
        });
        return retry;
      } else {
        throw new Error('Session expired');
      }
    }

    return response;
  } catch (err) {
    console.error('Fetch with refresh failed:', err);
    throw err;
  }
}
