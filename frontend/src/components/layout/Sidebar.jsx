// /frontend/src/components/layout/Sidebar.jsx
// Sidebar navigation component for dashboard layout

import { useState } from "react";
import { Link } from "react-router-dom";
import { FaBars, FaTimes, FaTachometerAlt, FaUser, FaSignOutAlt } from "react-icons/fa";

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => {
    setCollapsed((prev) => !prev);
  };

  return (
    <nav
      className={`sidebar bg-white text-black shadow-md ${
        collapsed ? "w-16" : "w-64"
      } transition-width duration-300`}
      aria-label="Main sidebar"
    >
      <div className="flex items-center justify-between p-4 border-b">
        {!collapsed && <h2 className="text-xl font-bold">JedgeBot</h2>}
        <button onClick={toggleSidebar} aria-label="Toggle sidebar">
          {collapsed ? <FaBars /> : <FaTimes />}
        </button>
      </div>

      <ul className="p-4 space-y-4">
        <li>
          <Link to="/dashboard" className="flex items-center gap-2">
            <FaTachometerAlt />
            {!collapsed && <span>Dashboard</span>}
          </Link>
        </li>
        <li>
          <Link to="/profile" className="flex items-center gap-2">
            <FaUser />
            {!collapsed && <span>Profile</span>}
          </Link>
        </li>
        <li>
          <button className="flex items-center gap-2">
            <FaSignOutAlt />
            {!collapsed && <span>Logout</span>}
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default Sidebar;
