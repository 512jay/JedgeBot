// /frontend/src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from "react";
import PropTypes from "prop-types";
import { fetchWithRefresh } from "../utils/authHelpers";
import { logout as logoutApi } from "../api/auth_api";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext(); // <-- This was missing before

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const response = await fetchWithRefresh("/auth/me", {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch user");
        }

        const data = await response.json();
        setUser(data);
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

  const navigate = useNavigate();

  const logout = async () => {
    try {
      await logoutApi(); // Calls /auth/logout
      setUser(null);
      navigate("/login");
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
