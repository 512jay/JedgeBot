// /frontend/src/pages/Dashboard.jsx
// Role-based dashboard entry point with integrated sidebar layout

import React from "react";
import { Navigate } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import { useAuth } from "../context/AuthContext";
import ClientDashboard from "../views/ClientDashboard";
import FreeDashboard from "../views/FreeDashboard";
import ManagerDashboard from "../views/ManagerDashboard";
import EnterpriseDashboard from "../views/EnterpriseDashboard";

useEffect(() => {
  document.title = "Dashboard - JedgeBot";
}, []);


export default function Dashboard() {
  const { user, loading } = useAuth();

  if (loading) return <p>Loading dashboard...</p>;
  if (!user) return <Navigate to="/login" />;

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="w-full p-6">
        <h1 className="text-3xl font-bold mb-6">Welcome to your Dashboard</h1>
        {user.role === "free" && <FreeDashboard />}
        {user.role === "client" && <ClientDashboard />}
        {user.role === "manager" && <ManagerDashboard />}
        {user.role === "enterprise" && <EnterpriseDashboard />}
      </main>
    </div>
  );
}