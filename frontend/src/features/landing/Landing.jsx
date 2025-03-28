// /frontend/src/features/landing/Landing.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import WaitlistForm from './WaitlistForm';
import '@/styles/Landing.css';
import '@/styles/global.css';
import {
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBNavbarItem,
  MDBContainer,
  MDBFooter
} from 'mdb-react-ui-kit';

export default function Landing() {
  return (
    <div className="bg-mutedRose min-vh-100 d-flex flex-column">
      {/* Top Navbar */}
      <MDBNavbar expand="lg" light bgColor="light" className="landing-navbar shadow-sm">
        <MDBContainer>
          <MDBNavbarBrand tag={Link} to="/" className="fw-bold" style={{ color: '#9A616D' }}>
            Fordis Ludus
          </MDBNavbarBrand>
          <MDBNavbarNav right fullWidth={false} className="d-flex flex-row gap-3">
            <MDBNavbarItem><Link className="nav-link" to="/about">About</Link></MDBNavbarItem>
            <MDBNavbarItem><Link className="nav-link" to="/pricing">Pricing</Link></MDBNavbarItem>
            <MDBNavbarItem><Link className="nav-link" to="/contact">Contact</Link></MDBNavbarItem>
            <MDBNavbarItem><Link className="nav-link" to="/login">Login</Link></MDBNavbarItem>
            <MDBNavbarItem><Link className="nav-link" to="/register">Register</Link></MDBNavbarItem>
          </MDBNavbarNav>
        </MDBContainer>
      </MDBNavbar>

      {/* Main Split Section */}
      <div className="flex-grow-1 d-flex justify-content-center align-items-center landing-split">
        <div className="landing-card shadow-lg">
          <div className="image-section">
            <img
              src="/images/landing-side.jpg"
              alt="Welcome to Fordis Ludus"
              className="img-fluid h-100 w-100 object-cover rounded-start"
            />
          </div>
          <div className="form-section p-4">
            <h2 className="mb-3 text-center">Fordis Ludus</h2>
            <p className="mb-4 text-center">Multi-Broker Trading. Automated. Intelligent.</p>
            <WaitlistForm />
          </div>
        </div>
      </div>

      {/* Footer */}
      <MDBFooter className="text-center text-white py-3" style={{ backgroundColor: '#9A616D' }}>
        © {new Date().getFullYear()} Fordis Ludus &nbsp;|&nbsp;
        <Link to="/terms" className="text-white text-decoration-underline">Terms</Link> &nbsp;|&nbsp;
        <Link to="/privacy" className="text-white text-decoration-underline">Privacy</Link> &nbsp;|&nbsp;
        <Link to="/contact" className="text-white text-decoration-underline">Contact</Link>
      </MDBFooter>
    </div>
  );
}
