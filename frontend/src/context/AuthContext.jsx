// /frontend/src/context/AuthContext.jsx
import PropTypes from "prop-types";
import React, { createContext, useContext, useEffect, useState } from "react";
import { logout as logoutApi } from "@auth/auth_api";
import { fetchWithRefresh } from "@/utils/authHelpers";
const BASE_URL = import.meta.env.VITE_API_URL;

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  const fetchUser = async () => {
    const hasSession = document.cookie.includes("has_session=1");

    if (!hasSession) {
      setLoading(false); // Skip fetching entirely for first-time users
      return;
    }

    try {
      setLoading(true);
      const response = await fetchWithRefresh(`${BASE_URL}/auth/me`, {
        method: "GET",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to fetch user");
      }

      let data = null;
      try {
        data = await response.json();
        setUser(data);
      } catch {
        console.warn("Failed to parse JSON response from /auth/me");
        setUser(null);
      }
    } catch (err) {
      console.error("Failed to fetch user in AuthContext", err);
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

  const value = { user, loading, error, setUser, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export const useAuth = () => useContext(AuthContext);
