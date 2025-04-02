// /frontend/src/features/auth/auth_api.js
// Provides reusable async functions to interact with the backend authentication API.

import { fetchWithCredentials } from "@/api/api_client"; // Shared utility for fetch requests with cookies included

// Use environment variable or fallback to localhost
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Registers a new user with the backend
 * @param {Object} userData - { email, password, username }
 * @returns {Promise<Response>}
 */
export async function register(userData) {
  return fetchWithCredentials(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json", },
    body: JSON.stringify(userData),
  });
}

/**
 * Logs in a user by sending credentials to the backend
 * @param {string} email
 * @param {string} password
 * @returns {Promise<Object>} Auth data from server
 * @throws {Error} Throws error if response is not OK
 */
export async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    credentials: "include", // include cookies for session
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  // Centralized error handling with detail fallback
  if (!response.ok) {
    const error = new Error(data?.detail || "Login failed");
    error.status = response.status;
    error.detail = data?.detail;
    throw error;
  }

  return data;
}

/**
 * Logs out the current user
 * @returns {Promise<Response>}
 */
export async function logoutApi() {
  console.log("Calling /auth/logout...");
  const res = await fetch(`${API_URL}/auth/logout`, {
    method: "POST",
    credentials: "include",
  });
  console.log("Response status:", res.status);

  if (!res.ok) {
    throw new Error("Logout failed");
  }
}


/**
 * Checks if the user is currently authenticated
 * @returns {Promise<Response>} User object or error
 */
export async function checkAuthentication() {
  return fetchWithCredentials(`${API_URL}/auth/check`);
}

/**
 * Attempts to refresh the user's access token
 * @returns {Promise<Response>} New token or error
 */
export async function refreshToken() {
  return fetchWithCredentials(`${API_URL}/auth/refresh`, {
    method: "POST",
  });
}
