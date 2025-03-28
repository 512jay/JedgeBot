// /frontend/src/components/layouts/PublicLayout.jsx
import React, { useEffect } from "react";
import { Outlet, useLocation, Link } from "react-router-dom";
import {
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBNavbarItem,
  MDBContainer,
  MDBFooter,
} from "mdb-react-ui-kit";
import { useAuth } from "@/context/useAuth"; // Adjust path to your auth hook if needed

export default function PublicLayout({
  pageTitle = "Fordis Ludus",
  children,
  hideHeader = false,
  hideFooter = false,
  debug = false,
  hero = false,
}) {
  const location = useLocation();
  const { user } = useAuth?.() || {};

  useEffect(() => {
    document.title = pageTitle;
  }, [pageTitle]);

  return (
    <div className={`min-vh-100 d-flex flex-column ${hero ? "hero-layout" : "bg-mutedRose"}`}>
      {/* Optional Header */}
      {!hideHeader && (
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
                  <Link className="nav-link fw-semibold" to="/dashboard">
                    Back to Dashboard
                  </Link>
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
      )}

      {/* Main Content */}
      <main className="flex-grow-1 d-flex justify-content-center align-items-center p-3">
        {children || <Outlet />}
      </main>

      {/* Optional Debug Info */}
      {debug && (
        <pre className="text-muted small text-center">
          Debug Mode: path={location.pathname}, auth={user?.isAuthenticated ? "yes" : "no"}
        </pre>
      )}

      {/* Optional Footer */}
      {!hideFooter && (
        <MDBFooter className="text-center text-white py-3" style={{ backgroundColor: "#9A616D" }}>
          © {new Date().getFullYear()} Fordis Ludus &nbsp;|&nbsp;
          <Link to="/terms" className="text-white text-decoration-underline">Terms</Link> &nbsp;|&nbsp;
          <Link to="/privacy" className="text-white text-decoration-underline">Privacy</Link> &nbsp;|&nbsp;
          <Link to="/contact" className="text-white text-decoration-underline">Contact</Link>
        </MDBFooter>
      )}
    </div>
  );
}
