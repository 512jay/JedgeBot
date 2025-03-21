// /frontend/src/pages/Dashboard.jsx
import React, { useState } from "react";
import Sidebar from "@/components/Sidebar";
import DashboardCards from "@/components/DashboardCards";

const Dashboard = () => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <Sidebar onToggleCollapse={() => setCollapsed(!collapsed)} />

      {/* Main content adjusts to sidebar width */}
      <div className={`p-6 transition-all duration-300 ${collapsed ? "ml-16" : "ml-64"}`}>
        <h1 className="text-3xl font-bold mb-6">Welcome to your Dashboard</h1>
        <DashboardCards />
      </div>
    </div>
  );
};

export default Dashboard;
