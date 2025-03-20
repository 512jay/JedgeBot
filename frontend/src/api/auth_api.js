// frontend/src/api/auth_api.js
// API functions to handle authentication, such as login, logout, and fetching protected data.
// This file contains functions to handle authentication, such as login, logout, and fetching protected data.

const API_URL = import.meta.env.VITE_API_URL;

export const register = async (email, password) => {
  const response = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    credentials: "include", // Ensures cookies are sent with the request
  });

  return response.json();
};

export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
    credentials: "include", // Ensures cookies are used
  });

  if (!response.ok) {
    throw new Error("Invalid login credentials");
  }

  return response.json();
}

export async function fetchProtectedData() {
  const response = await fetch(`${API_URL}/clients/some-protected-route`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include", // Ensures authentication via cookies
  });

  if (!response.ok) {
    throw new Error("Failed to fetch protected data");
  }

  return await response.json();
}

export async function logout() {
  const response = await fetch(`${API_URL}/auth/logout`, {
    method: "POST",
    credentials: "include", // Ensures the cookie is cleared properly
  });

  if (!response.ok) {
    throw new Error("Logout failed");
  }
}
