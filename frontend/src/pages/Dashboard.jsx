// /frontend/src/pages/Dashboard.jsx
// Role-based dashboard entry point, redirects if no valid role

import React from "react";
import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";
import FreeDashboard from "../views/dashboard/FreeDashboard";
import ClientDashboard from "../views/dashboard/ClientDashboard";
import ManagerDashboard from "../views/dashboard/ManagerDashboard";
import EnterpriseDashboard from "../views/dashboard/EnterpriseDashboard";

const Dashboard = () => {
  const { user, loading } = useAuth();

  if (loading) return <p className="p-6">Loading dashboard...</p>;
  if (!user) return <Navigate to="/login" />;

  switch (user.role) {
    case "client":
      return <ClientDashboard />;
    case "manager":
      return <ManagerDashboard />;
    case "enterprise":
      return <EnterpriseDashboard />;
    case "free":
      return <FreeDashboard />;
    default:
      return <Navigate to="/login" />;
  }
};

export default Dashboard;
