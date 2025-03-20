// frontend/src/api/api.jsx
// API functions to interact with the backend
// This file contains functions to interact with the backend API, such as fetching data or sending requests.

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const login = async (email, password) => {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                grant_type: "password",
                username: email,
                password: password,
            }),
        });

        if (!response.ok) {
            throw new Error("Invalid login credentials");
        }

        return await response.json();
    } catch (error) {
        console.error("Login failed:", error);
        return null;
    }
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
