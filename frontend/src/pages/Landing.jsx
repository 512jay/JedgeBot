// /frontend/src/pages/Landing.jsx
// Landing page for the project using MDB React

import React from "react";
import { Link } from "react-router-dom";
import { MDBContainer, MDBBtn, MDBTypography } from "mdb-react-ui-kit";
import "../styles/Landing.css"; // Ensure you have some styles for the landing page

function Landing() {
  return (
    <MDBContainer className="landing-container text-center py-5">
      <header className="landing-header">
        <MDBTypography tag="h1" className="mb-4">Welcome to JedgeBot</MDBTypography>
        <MDBTypography tag="p" className="mb-4">
          Your ultimate trading automation and portfolio management tool.
        </MDBTypography>
        <div className="landing-buttons">
          <Link to="/login">
            <MDBBtn color="primary" className="me-3">Login</MDBBtn>
          </Link>
          <Link to="/register">
            <MDBBtn color="secondary">Sign Up</MDBBtn>
          </Link>
        </div>
      </header>
    </MDBContainer>
  );
}

export default Landing;