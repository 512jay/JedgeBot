const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchMessage = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};
