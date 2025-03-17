// File: frontend/src/components/Sidebar.jsx
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  MDBListGroup,
  MDBListGroupItem,
  MDBIcon,
  MDBBtn,
} from "mdb-react-ui-kit";
import "../styles/Sidebar.css";

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();  // For navigation after logout

  const handleLogout = () => {
    localStorage.removeItem("access_token");  // Clear token
    navigate("/login");                       // Redirect to login
    window.location.reload();                 // Refresh UI
  };

  return (
    <div className={`sidebar d-flex flex-column ${collapsed ? "collapsed" : ""}`}>
      <MDBBtn
        className="toggle-btn"
        color="primary"
        onClick={() => setCollapsed(!collapsed)}
      >
        <MDBIcon fas icon={collapsed ? "angle-right" : "angle-left"} />
      </MDBBtn>

      <h4 className={`text-center ${collapsed ? "d-none" : ""}`}>JedgeBot</h4>

      <MDBListGroup flush="true">
        <Link to="/dashboard">
          <MDBListGroupItem action>
            <MDBIcon fas icon="chart-line" className="me-3" />{" "}
            {!collapsed && "Dashboard"}
          </MDBListGroupItem>
        </Link>
        <Link to="/clients">
          <MDBListGroupItem action>
            <MDBIcon fas icon="users" className="me-3" /> {!collapsed && "Clients"}
          </MDBListGroupItem>
        </Link>
        <Link to="/markets">
          <MDBListGroupItem action>
            <MDBIcon fas icon="globe" className="me-3" /> {!collapsed && "Markets"}
          </MDBListGroupItem>
        </Link>
        <Link to="/settings">
          <MDBListGroupItem action>
            <MDBIcon fas icon="cog" className="me-3" /> {!collapsed && "Settings"}
          </MDBListGroupItem>
        </Link>

        {/* Logout Button */}
        <MDBListGroupItem action className="mt-auto" onClick={handleLogout}>
          <MDBIcon fas icon="sign-out-alt" className="me-3" /> {!collapsed && "Logout"}
        </MDBListGroupItem>
      </MDBListGroup>
    </div>
  );
};

export default Sidebar;
