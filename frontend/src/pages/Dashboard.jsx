// /frontend/src/pages/Dashboard.jsx
import React from "react";
import { Outlet } from "react-router-dom"; // Allows nested routes to render inside the Dashboard
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

function DashboardLayout() {
  console.log("🖥️ DashboardLayout: Rendering...");

  return (
    <div className="dashboard-container d-flex">
      <Sidebar />
      <div className="main-content flex-grow-1">
        <Navbar />
        <div className="content p-4">
          <Outlet /> {/* 👈 This is where sub-pages like Home, Profile, etc. will be rendered */}
        </div>
      </div>
    </div>
  );
}

export default DashboardLayout;
