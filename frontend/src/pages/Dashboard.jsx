// /frontend/src/pages/Dashboard.jsx
// Main dashboard page that renders user-specific views with sidebar navigation.

import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import Sidebar from "../components/layout/Sidebar";

import FreeDashboard from "../views/FreeDashboard";
import ClientDashboard from "../views/ClientDashboard";
import ManagerDashboard from "../views/ManagerDashboard";
import EnterpriseDashboard from "../views/EnterpriseDashboard";

const Dashboard = () => {
  const { user } = useAuth();

  useEffect(() => {
    document.title = "Dashboard - JedgeBot";
  }, []);

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar />

      <main className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-4">Welcome to your dashboard</h1>

        {user?.role === "client" && <ClientDashboard />}
        {user?.role === "manager" && <ManagerDashboard />}
        {user?.role === "enterprise" && <EnterpriseDashboard />}
        {(!user?.role || user?.role === "free") && <FreeDashboard />}
      </main>
    </div>
  );
};

export default Dashboard;
