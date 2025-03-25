// /frontend/src/components/layout/Sidebar.jsx
import React, { useState } from "react";
import {
  MDBIcon,
  MDBListGroup,
  MDBListGroupItem,
  MDBCollapse,
  MDBBtn,
} from "mdb-react-ui-kit";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();
  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  return (
    <div
      style={{
        width: collapsed ? "70px" : "250px",
        backgroundColor: "#9A616D",
        color: "white",
        padding: collapsed ? "1rem 0" : "1rem",
        transition: "width 0.3s ease",
        display: "flex",
        flexDirection: "column",
        alignItems: collapsed ? "center" : "flex-start",
        height: "100vh",
      }}
    >
<h3
  onClick={toggleSidebar}
  style={{
    fontSize: "1.5rem",
    fontWeight: "bold",
    marginBottom: "2rem",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: collapsed ? "center" : "space-between",
    width: "100%",
  }}
>
  {collapsed ? (
    <>
      JB&nbsp;
      <MDBIcon icon="angle-double-right" />
    </>
  ) : (
    <>
      JedgeBot
      <MDBIcon icon="angle-double-left" />
    </>
  )}
</h3>

      <MDBListGroup style={{ width: "100%" }}>
        <MDBListGroupItem tag="div" style={{ background: "transparent", border: "none" }}>
          <Link to="/dashboard" style={{ color: "white", textDecoration: "none" }}>
            <MDBIcon icon="tachometer-alt" className="me-2 " />
            {!collapsed && "Dashboard"}
          </Link>
        </MDBListGroupItem>

        <MDBListGroupItem tag="div" style={{ background: "transparent", border: "none" }}>
          <Link to="/profile" style={{ color: "white", textDecoration: "none" }}>
            <MDBIcon icon="user" className="me-2" />
            {!collapsed && "Profile"}
          </Link>
        </MDBListGroupItem>

        <MDBListGroupItem tag="div" style={{ background: "transparent", border: "none" }}>
          <button
            onClick={handleLogout}
            style={{
              background: "black",
              color: "white",
              padding: collapsed ? "0.5rem" : "0.5rem 1rem",
              borderRadius: "5px",
              border: "none",
              cursor: "pointer",
              width: collapsed ? "auto" : "100%",
              marginTop: "1rem",
            }}
          >
            <MDBIcon icon="sign-out-alt" className="me-2" />
            {!collapsed && "Logout"}
          </button>
        </MDBListGroupItem>
      </MDBListGroup>
    </div>
  );
};

export default Sidebar;