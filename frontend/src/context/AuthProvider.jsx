// /frontend/src/context/AuthProvider.jsx
import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { fetchWithRefresh } from "@/utils/fetchWithRefresh";
import { logoutApi } from "@auth/auth_api";
import { AuthContext } from "./auth-context";

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const checkAuth = useCallback(async () => {
  const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const hasSession = document.cookie.includes("has_session=1");
  if (!hasSession) {
    setUser(null);
    setLoading(false);
    return;
  }

  try {
    setLoading(true);
    const response = await fetchWithRefresh(`${BASE_URL}/auth/me`, {
      method: "GET",
      credentials: "include",
    });

    const data = await response.json();
    setUser(data);
  } catch (err) {
    console.error("AuthContext fetch error:", err);
    setUser(null);
    setError(err.message);
  } finally {
    setLoading(false);
  }
}, [setUser, setLoading, setError]);


  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

const logout = async () => {
  console.log("Logging out...");
  await logoutApi(); // or await logout() if you're keeping the import name
  console.log("Clearing user context...");
  setUser(null);
  navigate("/login");
};

  return (
    <AuthContext.Provider
      value={{ user, loading, error, setUser, logout, checkAuth }}
    >
      {children}
    </AuthContext.Provider>
  );
};
