// frontend/src/api/api_client.js
// API functions to interact with the backend
// This file contains functions to interact with the backend API, such as fetching data or sending requests.

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const login = async (email, password) => {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },  // ✅ Use JSON
        body: JSON.stringify({ email, password }),  // ✅ Match FastAPI backend
        credentials: "include", // ✅ Ensures cookies are sent
    });

    if (!response.ok) {
        throw new Error("Invalid login credentials");
    }
    return await response.json();
};

export const fetchMessage = async () => {
    try {
        const response = await fetch(`${API_URL}/`);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};
