// /frontend/src/utils/fetchWithCredentials.js
// Global helper for fetch requests with cookies and error handling

export default async function fetchWithCredentials(url, options = {}) {
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
  