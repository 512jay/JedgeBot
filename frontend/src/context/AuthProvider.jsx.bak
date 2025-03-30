// /frontend/src/context/AuthProvider.jsx
import PropTypes from "prop-types";
import React, { useState, useEffect } from "react";
import { AuthContext } from "./auth-context";
import { logout as logoutApi } from "@auth/auth_api";
import { fetchWithRefresh } from "@/utils/authHelpers";

const BASE_URL = import.meta.env.VITE_API_URL;

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      const hasSession = document.cookie.includes("has_session=1");
      if (!hasSession) return setLoading(false);

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
    };

    fetchUser();
  }, []);

  const logout = async () => {
    try {
      await logoutApi();
      setUser(null);
    } catch (err) {
      console.error("Logout failed", err);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};
