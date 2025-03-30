// /frontend/src/components/layouts/Header.jsx
import React from "react";
import { Link } from "react-router-dom";
import {
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBNavbarItem,
  MDBContainer,
} from "mdb-react-ui-kit";
import { useAuth } from "@/context/useAuth";

export default function Header() {
  const { user } = useAuth?.() || {};

  return (
    <MDBNavbar expand="lg" light bgColor="light" className="shadow-sm">
      <MDBContainer>
        <MDBNavbarBrand tag={Link} to="/" className="fw-bold" style={{ color: "#9A616D" }}>
          Fordis Ludus
        </MDBNavbarBrand>
        <MDBNavbarNav right fullWidth={false} className="d-flex flex-row gap-3">
          <MDBNavbarItem><Link className="nav-link" to="/about">About</Link></MDBNavbarItem>
          <MDBNavbarItem><Link className="nav-link" to="/pricing">Pricing</Link></MDBNavbarItem>
          <MDBNavbarItem><Link className="nav-link" to="/contact">Contact</Link></MDBNavbarItem>
          {user?.isAuthenticated ? (
            <MDBNavbarItem>
              <Link className="nav-link fw-semibold" to="/dashboard">Back to Dashboard</Link>
            </MDBNavbarItem>
          ) : (
            <>
              <MDBNavbarItem><Link className="nav-link" to="/login">Login</Link></MDBNavbarItem>
              <MDBNavbarItem><Link className="nav-link" to="/register">Register</Link></MDBNavbarItem>
            </>
          )}
        </MDBNavbarNav>
      </MDBContainer>
    </MDBNavbar>
  );
}
