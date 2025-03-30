// /frontend/src/components/layouts/DashboardLayout.jsx
import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "@/components/layouts/Sidebar";
import { useAuth } from "@hooks/useAuth";

export default function DashboardLayout({ children }) {
  const { user } = useAuth?.() || {};

  // Decide layout type based on role (can be made more dynamic later)
  const useSidebar = user?.role === "manager" || user?.role === "enterprise";

  return (
    <div className="dashboard-layout d-flex min-vh-100 bg-light">
      {/* Sidebar for manager/enterprise roles */}
      {useSidebar && (
        <aside className="sidebar shadow-sm">
          <Sidebar />
        </aside>
      )}

      {/* Main content area */}
      <main className="flex-grow-1 p-3">
        {children || <Outlet />}
      </main>
    </div>
  );
}
