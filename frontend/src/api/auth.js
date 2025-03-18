// frontend/src/api/auth.js
const API_URL = import.meta.env.VITE_API_URL;

export const register = async (email, password) => {
  const response = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  return response.json();
};

export const login = async (email, password) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: new URLSearchParams({ username: email, password }), // OAuth2 uses FormData
  });

  return response.json();
};
