// /frontend/src/features/landing/Landing.jsx
import React, { useState } from "react";
import {
  MDBContainer,
  MDBInput,
  MDBBtn
} from "mdb-react-ui-kit";
import "@styles/Landing.css";

const heroImage = "/images/hero/welcomejedgebot.jpg"; // public image path

export default function Landing() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [message, setMessage] = useState("");
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Waitlist form submitted:", { email, name, role, message });

    setEmail("");
    setName("");
    setRole("");
    setMessage("");
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 3500);
  };

  return (
    <MDBContainer className="landing-split d-flex flex-column align-items-center justify-content-center py-5">
      <div className="landing-card">
        {/* Hero Image */}
        <div className="image-section">
          <img
            src={heroImage}
            alt="Fordis Ludus dashboard"
            className="img-fluid h-100 w-100 object-cover"
          />
        </div>

        {/* Waitlist Form */}
        <div className="form-section p-4 p-md-5">
          <h3 className="text-center fw-bold mb-3">Fordis Ludus</h3>
          <p className="text-center text-muted mb-4">
            Multi-Broker Trading. Automated. Intelligent.
          </p>

          <form onSubmit={handleSubmit}>
            <MDBInput
              label="Email"
              type="email"
              className="mb-3"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <MDBInput
              label="Name (optional)"
              type="text"
              className="mb-3"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <div className="form-outline mb-3">
              <label className="form-label" htmlFor="role">
                Select Role
              </label>
              <select
                id="role"
                className="form-select"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                required
              >
                <option value="">Choose...</option>
                <option value="client">Client</option>
                <option value="manager">Manager</option>
                <option value="enterprise">Enterprise</option>
                <option value="other">Other</option>
              </select>
            </div>

            <MDBInput
              label="What would you like to see in Fordis Ludus?"
              type="text"
              className="mb-3"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />

            <MDBBtn type="submit" className="w-100 bg-primary">
              JOIN THE WAITLIST
            </MDBBtn>

            {showSuccess && (
              <div className="alert alert-success mt-3" role="alert">
                🎉 You’re on the list! Thanks for believing in Fordis Ludus.
              </div>
            )}
          </form>
        </div>
      </div>
    </MDBContainer>
  );
}
