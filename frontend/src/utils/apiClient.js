// /frontend/src/utils/apiClient.js
// Central API client that always uses fetchWithRefresh for protected routes

import { fetchWithRefresh } from "../utils/fetchWithRefresh";
import { config } from "@/config";

const apiClient = {
  get: async (url, options = {}) => {
    return fetchWithRefresh(`${config.API_URL}${url}`, {
      method: "GET",
      ...options,
    });
  },

  post: async (url, body, options = {}) => {
    return fetchWithRefresh(`${config.API_URL}${url}`, {
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
    return fetchWithRefresh(`${config.API_URL}${url}`, {
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
    return fetchWithRefresh(`${config.API_URL}${url}`, {
      method: "DELETE",
      ...options,
    });
  },
};

export default apiClient;
