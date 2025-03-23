// /frontend/src/components/Sidebar.jsx
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  MDBListGroup,
  MDBListGroupItem,
  MDBIcon,
  MDBBtn,
} from "mdb-react-ui-kit";
import "../styles/Sidebar.css";

const Sidebar = ({ onAddClient }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
    window.location.reload();
  };

  return (
    <nav className={`sidebar ${collapsed ? "collapsed" : ""}`} aria-label="Main sidebar">
      <MDBBtn
        className="toggle-btn m-2"
        color="primary"
        onClick={() => setCollapsed(!collapsed)}
      >
        <MDBIcon fas icon={collapsed ? "angle-right" : "angle-left"} />
      </MDBBtn>

      <h4 className={`text-center py-2 ${collapsed ? "d-none" : ""}`}>JedgeBot</h4>

      <MDBListGroup className="flex-grow-1">
        <Link to="/dashboard">
          <MDBListGroupItem action>
            <MDBIcon fas icon="chart-line" className="me-3" />
            {!collapsed && "Dashboard"}
          </MDBListGroupItem>
        </Link>
        <Link to="/accounts">
          <MDBListGroupItem action>
            <MDBIcon fas icon="money-check-alt" className="me-3" />
            {!collapsed && "Accounts"}
          </MDBListGroupItem>
        </Link>
        <Link to="/clients">
          <MDBListGroupItem action>
            <MDBIcon fas icon="users" className="me-3" />
            {!collapsed && "Clients"}
          </MDBListGroupItem>
        </Link>
        <Link to="/markets">
          <MDBListGroupItem action>
            <MDBIcon fas icon="globe" className="me-3" />
            {!collapsed && "Markets"}
          </MDBListGroupItem>
        </Link>
        <Link to="/settings">
          <MDBListGroupItem action>
            <MDBIcon fas icon="cog" className="me-3" />
            {!collapsed && "Settings"}
          </MDBListGroupItem>
        </Link>
      </MDBListGroup>

      {/* New Client Button */}
      <div className="p-2">
        <MDBBtn color="success" className="w-100" onClick={onAddClient}>
          <MDBIcon fas icon="user-plus" className="me-2" />
          {!collapsed && "New Client"}
        </MDBBtn>
      </div>

      {/* Logout Button */}
      <div className="logout-btn-container p-2">
        <MDBBtn color="danger" className="w-100" onClick={handleLogout}>
          <MDBIcon fas icon="sign-out-alt" className="me-2" />
          {!collapsed && "Logout"}
        </MDBBtn>
      </div>
    </nav>
  );
};

export default Sidebar;
