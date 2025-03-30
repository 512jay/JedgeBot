// /frontend/src/components/auth/PrivateRoute.jsx
import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/context/useAuth";
import LoadingScreen from "@/components/layouts/LoadingScreen"; // optional loading component

const PrivateRoute = () => {
  const { user, loading } = useAuth();

  if (loading) return <LoadingScreen />; // optional UX

  return user ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
