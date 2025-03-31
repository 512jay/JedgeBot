// /frontend/src/utils/fetchWithRefresh.js
// Wrapper for fetch that optionally retries once if session is expired

export async function fetchWithRefresh(url, options = {}) {
  const response = await fetch(url, options);

  // If session expired, attempt to refresh and retry once
  if (response.status === 401) {
    try {
      const refresh = await fetch("/auth/refresh", {
        method: "POST",
        credentials: "include",
      });

      if (refresh.ok) {
        return fetch(url, options); // Retry original request
      }
    } catch (err) {
      console.error("Token refresh failed:", err);
    }
  }

  return response;
}
