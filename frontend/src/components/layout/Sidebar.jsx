// /frontend/components/layout/Sidebar.jsx
import React, { useState } from "react";
import { MDBIcon } from "mdb-react-ui-kit";
import { Link } from "react-router-dom";

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const toggleSidebar = () => setCollapsed(!collapsed);

  return (
    <div
      className={`h-full bg-mutedRose text-white transition-all duration-300 flex flex-col ${
        collapsed ? "w-16" : "w-64"
      }`}
    >
      <div className="flex items-center justify-between p-4 border-b border-white/20">
        {!collapsed && <h2 className="text-xl font-bold">JedgeBot</h2>}
        <button onClick={toggleSidebar}>
          <MDBIcon fas icon="bars" />
        </button>
      </div>

      <nav className="flex-1 flex flex-col gap-4 p-4">
        <Link to="/dashboard" className="flex items-center gap-3 hover:text-gray-300">
          <MDBIcon fas icon="tachometer-alt" />
          {!collapsed && <span>Dashboard</span>}
        </Link>
        <Link to="/profile" className="flex items-center gap-3 hover:text-gray-300">
          <MDBIcon fas icon="user" />
          {!collapsed && <span>Profile</span>}
        </Link>
        <Link to="/logout" className="flex items-center gap-3 hover:text-gray-300">
          <MDBIcon fas icon="sign-out-alt" />
          {!collapsed && <span>Logout</span>}
        </Link>
      </nav>
    </div>
  );
};

export default Sidebar;
