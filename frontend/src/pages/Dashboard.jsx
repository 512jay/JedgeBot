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
      <div className={`transition-all duration-300 w-full ${collapsed ? "pl-16" : "pl-64"} p-6`}>
        <h1 className="text-3xl font-bold mb-6">Welcome to your Dashboard</h1>
        <div className="bg-pink-500 text-white p-4">Tailwind is working 🎉</div>

        <DashboardCards />
      </div>
    </div>
  );
};

export default Dashboard;
