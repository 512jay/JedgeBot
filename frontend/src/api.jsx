//frontend/src/api/api.jsx
const API_URL = import.meta.env.VITE_API_URL;


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
