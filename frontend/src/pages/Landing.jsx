// /frontend/src/pages/Landing.jsx
// Landing page for the project using MDB React

import React from "react";
import { Link } from "react-router-dom";
import {
  MDBNavbar,
  MDBContainer,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBNavbarItem,
  MDBNavbarLink,
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBCardImage,
} from "mdb-react-ui-kit";
import "../styles/Landing.css";

const Landing = () => {
  return (
    <div className="landing-page">
      {/* MDB Navbar */}
      <MDBNavbar light bgColor="light">
        <MDBContainer>
          <MDBNavbarBrand tag={Link} to="/">JedgeBot</MDBNavbarBrand>
          <MDBNavbarNav className="d-flex flex-row gap-3">
            <MDBNavbarItem>
              <MDBNavbarLink tag={Link} to="/about">About</MDBNavbarLink>
            </MDBNavbarItem>
            <MDBNavbarItem>
              <MDBNavbarLink tag={Link} to="/pricing">Pricing</MDBNavbarLink>
            </MDBNavbarItem>
            <MDBNavbarItem>
              <MDBNavbarLink tag={Link} to="/how-it-works">How it Works</MDBNavbarLink>
            </MDBNavbarItem>
            <MDBNavbarItem>
              <MDBNavbarLink tag={Link} to="/login">Login</MDBNavbarLink>
            </MDBNavbarItem>
            <MDBNavbarItem>
              <MDBBtn tag={Link} to="/register" size="sm" color="primary">Sign Up</MDBBtn>
            </MDBNavbarItem>
          </MDBNavbarNav>
        </MDBContainer>
      </MDBNavbar>

      {/* Hero Section */}
      <MDBContainer className="d-flex justify-content-center align-items-center py-5">
        <MDBCard className="text-center shadow-3" style={{ maxWidth: "600px" }}>
          <MDBCardImage
            src="/images/welcomejedgebot.webp"
            alt="JedgeBot"
            position="top"
          />
          <MDBCardBody>
            <h2 className="mb-3">Welcome to JedgeBot</h2>
            <p className="mb-4">
              Your ultimate trading automation and portfolio management tool.
            </p>
            <div className="d-flex justify-content-center gap-3">
              <MDBBtn tag={Link} to="/login" color="primary">Login</MDBBtn>
              <MDBBtn tag={Link} to="/register" color="secondary">Sign Up</MDBBtn>
            </div>
          </MDBCardBody>
        </MDBCard>
      </MDBContainer>
    </div>
  );
};

export default Landing;
