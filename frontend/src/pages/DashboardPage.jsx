// /frontend/src/pages/DashboardPage.jsx
import React, { useState } from "react";
import Sidebar from "@/components/Sidebar";
import DashboardCards from "@/components/DashboardCards";

const DashboardPage = () => {
  const [collapsed, setCollapsed] = useState(false);

  // Pull role from localStorage or context
  const role = localStorage.getItem("role"); // TEMP: adjust when auth logic is formalized

  const renderDashboardContent = () => {
    switch (role) {
      case "client":
        return <div className="text-xl">Client-specific dashboard coming soon.</div>;
      case "manager":
        return <div className="text-xl">Manager view under construction.</div>;
      case "enterprise":
        return <div className="text-xl">Enterprise dashboard placeholder.</div>;
      default:
        return <DashboardCards />;
    }
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <Sidebar onToggleCollapse={() => setCollapsed(!collapsed)} />

      {/* Main content adjusts to sidebar width */}
      <div className={`p-6 transition-all duration-300 ${collapsed ? "ml-16" : "ml-64"}`}>
        <h1 className="text-3xl font-bold mb-6">Welcome to your Dashboard</h1>
        {renderDashboardContent()}
      </div>
    </div>
  );
};

export default DashboardPage;
