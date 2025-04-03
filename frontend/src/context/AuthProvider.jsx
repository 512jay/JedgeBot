// /frontend/src/context/AuthProvider.jsx
// Provides the user context and session-checking logic for the app.

import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { fetchWithRefresh } from "@/utils/fetchWithRefresh";
import { logoutApi } from "@auth/auth_api";
import { AuthContext } from "./auth-context";
import { wakeUpServer } from "@/utils/wakeUpServer";

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  /**
   * Loads the user from the backend using session cookies.
   * If no session exists, clears the user.
   */
  const loadUserSession = useCallback(async () => {
    try {
      setLoading(true);

      const response = await fetchWithRefresh(`${BASE_URL}/auth/me`, {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        console.warn("Session check failed:", response.status);
        throw new Error("Session expired or invalid");
      }

      const userData = await response.json();
      setUser(userData);
    } catch (err) {
      console.error("loadUserSession error:", err);
      setUser(null);
      setError(err.message || "Auth error");
    } finally {
      setLoading(false);
    }
  }, [BASE_URL]);

  useEffect(() => {
    const init = async () => {
      await wakeUpServer(); // 🟣 Global warm-up for cold backend
      await loadUserSession(); // 🔐 Proceed with session check
    };
  
    init();
  }, [loadUserSession]);

  const logout = async () => {
    await logoutApi();
    setUser(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        setUser,
        logout,
        loadUserSession,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
