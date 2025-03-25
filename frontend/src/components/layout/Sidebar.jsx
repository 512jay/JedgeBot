// /frontend/components/layout/Sidebar.jsx
import React, { useState } from "react";
import { FaBars, FaHome, FaUser, FaSignOutAlt } from "react-icons/fa";
import { Link } from "react-router-dom";
import { MDBIcon } from "mdb-react-ui-kit";

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => setCollapsed(prev => !prev);

  return (
    <div
      className={`h-screen bg-mutedRose text-white transition-all duration-300 ${
        collapsed ? 'w-16' : 'w-64'
      } flex flex-col shadow-lg fixed left-0 top-0 z-10`}
    >
      <div className="flex items-center justify-between p-4 border-b border-white/10">
        {!collapsed && <h1 className="text-xl font-bold">JedgeBot</h1>}
        <button onClick={toggleSidebar}>
          <FaBars className="text-white" />
        </button>
      </div>
      <nav className="flex-1 px-2 pt-4 space-y-4">
        <Link to="/dashboard" className="flex items-center gap-3 hover:text-gray-300">
          <FaHome />
          {!collapsed && <span>Dashboard</span>}
        </Link>
        <Link to="/profile" className="flex items-center gap-3 hover:text-gray-300">
          <FaUser />
          {!collapsed && <span>Profile</span>}
        </Link>
        <Link to="/logout" className="flex items-center gap-3 hover:text-gray-300">
          <FaSignOutAlt />
          {!collapsed && <span>Logout</span>}
        </Link>
      </nav>
    </div>
  );
};

export default Sidebar;
