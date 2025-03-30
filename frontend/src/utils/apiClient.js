// /frontend/src/utils/apiClient.js
// Central API client that always uses fetchWithRefresh for protected routes

import { fetchWithRefresh } from "../utils/fetchWithRefresh";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const apiClient = {
  get: async (url, options = {}) => {
    return fetchWithRefresh(`${API_BASE}${url}`, {
      method: "GET",
      ...options,
    });
  },

  post: async (url, body, options = {}) => {
    return fetchWithRefresh(`${API_BASE}${url}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      body: JSON.stringify(body),
      ...options,
    });
  },

  put: async (url, body, options = {}) => {
    return fetchWithRefresh(`${API_BASE}${url}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      body: JSON.stringify(body),
      ...options,
    });
  },

  delete: async (url, options = {}) => {
    return fetchWithRefresh(`${API_BASE}${url}`, {
      method: "DELETE",
      ...options,
    });
  },
};

export default apiClient;
