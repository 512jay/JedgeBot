// /frontend/src/pages/Dashboard.jsx
// Role-based dashboard entry point with integrated sidebar layout

import React from "react";
import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import FreeDashboard from "../views/dashboard/FreeDashboard";
import ClientDashboard from "../views/dashboard/ClientDashboard";
import ManagerDashboard from "../views/dashboard/ManagerDashboard";
import EnterpriseDashboard from "../views/dashboard/EnterpriseDashboard";

const Dashboard = () => {
  const { user, loading } = useAuth();

  if (loading) return <p className="p-6">Loading dashboard...</p>;
  if (!user) return <Navigate to="/login" />;

  const renderDashboardByRole = () => {
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

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-grow p-6 transition-all duration-300">
        {renderDashboardByRole()}
      </div>
    </div>
  );
};

export default Dashboard;
