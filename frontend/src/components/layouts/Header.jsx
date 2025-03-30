// /frontend/src/components/layouts/Header.jsx
import { useAuth } from "@hooks/useAuth";
import {
  MDBContainer,
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarItem,
  MDBNavbarNav,
} from "mdb-react-ui-kit";
import React from "react";
import { Link } from "react-router-dom";

export default function Header() {
  const { user, loading } = useAuth?.() || {};


  return (
    <MDBNavbar expand="lg" light bgColor="light" className="shadow-sm">
      <MDBContainer>
        <MDBNavbarBrand
          tag={Link}
          to="/"
          className="fw-bold"
          style={{ color: "#9A616D" }}
        >
          Fordis Ludus
        </MDBNavbarBrand>

        <MDBNavbarNav
  right
  fullWidth={false}
  className="d-flex flex-row gap-3"
  aria-label="Primary navigation"
>

          <MDBNavbarItem>
            <Link className="nav-link" to="/about" aria-label="About page">About</Link>
          </MDBNavbarItem>
          <MDBNavbarItem>
            <Link className="nav-link" to="/pricing" aria-label="Pricing page">Pricing</Link>
          </MDBNavbarItem>
          <MDBNavbarItem>
            <Link className="nav-link" to="/contact" aria-label="Contact page">Contact</Link>
          </MDBNavbarItem>

          {loading ? (
            <MDBNavbarItem>
              <span className="nav-link text-muted">Checking login...</span>
            </MDBNavbarItem>
          ) : user ? (
            <MDBNavbarItem>
              <Link className="nav-link fw-semibold text-primary" to="/dashboard" aria-label="Go to dashboard">
  Back to Dashboard
</Link>
            </MDBNavbarItem>
          ) : (
            <>
              <MDBNavbarItem>
                <Link className="nav-link" to="/login" aria-label="Login page">Login</Link>
              </MDBNavbarItem>
              <MDBNavbarItem>
                <Link className="nav-link" to="/register" aria-label="Register page">Register</Link>
              </MDBNavbarItem>
            </>
          )}

        </MDBNavbarNav>
      </MDBContainer>
    </MDBNavbar>
  );
}
