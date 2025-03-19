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

export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch("${API_URL}auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Invalid login credentials");
  }

  const data = await response.json();
  localStorage.setItem("token", data.access_token); // Save token in localStorage

  return data;
}

export async function fetchProtectedData() {
  const token = localStorage.getItem("token");

  const response = await fetch("${API_URL}/clients/some-protected-route", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`, // Send token in header
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch protected data");
  }

  return await response.json();
}


