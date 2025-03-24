// /frontend/src/views/DashboardView.jsx
import Sidebar from "@/components/Sidebar";
import { useAuth } from "@/context/AuthContext";
import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import ClientDashboard from "./ClientDashboard";
import FreeDashboard from "./dashboard/FreeDashboard";
import ManagerDashboard from "./ManagerDashboard";
import EnterpriseDashboard from "./EnterpriseDashboard";
./FreeDashboard

const DashboardView = () => {
  const [collapsed, setCollapsed] = useState(false);
  const { user, loading } = useAuth();

  if (loading) return <p className="p-6">Loading dashboard...</p>;
  if (!user) return <Navigate to="/login" replace />;

  const renderDashboardContent = () => {
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
      <Sidebar onToggleCollapse={() => setCollapsed(!collapsed)} />
      <div className={`p-6 transition-all duration-300 ${collapsed ? "ml-16" : "ml-64"}`}>
        <h1 className="text-3xl font-bold mb-6">Welcome to your Dashboard</h1>
        {renderDashboardContent()}
      </div>
    </div>
  );
};

export default DashboardView;
