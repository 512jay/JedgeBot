// /frontend/src/components/layouts/Footer.jsx
import React from "react";
import { Link } from "react-router-dom";
import { MDBFooter } from "mdb-react-ui-kit";

export default function Footer() {
  return (
    <MDBFooter className="text-center text-white py-3 mt-auto" style={{ backgroundColor: "#9A616D" }}>
      © {new Date().getFullYear()} Fordis Ludus &nbsp;|&nbsp;
      <Link to="/terms" className="text-white text-decoration-underline">Terms</Link> &nbsp;|&nbsp;
      <Link to="/privacy" className="text-white text-decoration-underline">Privacy</Link> &nbsp;|&nbsp;
      <Link to="/contact" className="text-white text-decoration-underline">Contact</Link>
    </MDBFooter>
  );
}
