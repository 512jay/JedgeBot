// /frontend/src/api/auth_api.js
// Handles authentication-related API calls (login, logout, register, token refresh)

import { fetchWithCredentials } from "../../api/api_client"; // ✅ Now using centralized request handler

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"; 

// Register request
export async function register(userData) {
    return fetchWithCredentials(`${API_URL}/auth/register`, {
        method: "POST",
        body: JSON.stringify(userData),
    });
}

// Login request
export async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    const error = new Error(data?.detail || "Login failed");
    error.status = response.status;
    error.detail = data?.detail;
    throw error;
  }

  return data;
}


// Logout request
export async function logout() {
    return fetchWithCredentials(`${API_URL}/auth/logout`, { method: "POST" });
}

// Check authentication status
export async function checkAuthentication() {
    return fetchWithCredentials(`${API_URL}/auth/check`);
}

// Refresh token
export async function refreshToken() {
    return fetchWithCredentials(`${API_URL}/auth/refresh`, { method: "POST" });
}
