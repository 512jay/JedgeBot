// /frontend/src/views/DashboardView.jsx
import React, { useState } from "react";
import Sidebar from "@/components/Sidebar";
import DashboardCards from "@/components/DashboardCards";
import { useAuth } from "@/context/AuthContext";
import { Navigate } from "react-router-dom";

const DashboardView = () => {
  const [collapsed, setCollapsed] = useState(false);
  const { user, loading } = useAuth();

  if (loading) return <p className="p-6">Loading dashboard...</p>;
  if (!user) return <Navigate to="/login" replace />;

  const renderDashboardContent = () => {
    switch (user.role) {
      case "client":
        return <div>Client-specific dashboard</div>;
      case "manager":
        return <div>Manager view under construction</div>;
      case "enterprise":
        return <div>Enterprise dashboard placeholder</div>;
      case "free":
        return <DashboardCards />;
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
