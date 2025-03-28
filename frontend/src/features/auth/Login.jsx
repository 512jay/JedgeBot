// /frontend/src/features/auth/Login.jsx
// Login form for user authentication

import React, { useState } from "react";
import {
  MDBCol,
  MDBRow,
  MDBInput,
  MDBBtn,
  MDBTypography
} from "mdb-react-ui-kit";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/useAuth";
import { login } from "@auth/auth_api";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const RESEND_ENDPOINT = `${API_URL}/auth/resend-verification`;

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [showResend, setShowResend] = useState(false); // 👈 added
  const navigate = useNavigate();
  const { setUser } = useAuth();

  const isVerificationError = (msg) =>
    typeof msg === "string" &&
    msg.toLowerCase().includes("email not verified");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    setShowResend(false);
    try {
      const response = await login(email, password);
      if (response.message === "Login successful") {
        setUser(response.user);
        navigate("/dashboard");
      } else {
        setError("Invalid credentials. Please try again.");
      }
    } catch (err) {
      const message =
        err?.detail ||
        err?.response?.data?.detail ||
        err?.message ||
        "Login failed. Please try again.";

      if (isVerificationError(message)) {
        setError("Email not verified. Please check your email to verify your account.");
        setShowResend(true);
      } else {
        setError(message);
      }
    }
  };

  const handleResendVerification = async () => {
    try {
      const res = await fetch(RESEND_ENDPOINT, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();
      setError(data.message || "Verification email resent.");
      setShowResend(false); // hide button after send
    } catch {
      setError("Failed to resend verification email. Please try again.");
    }
  };

return (
  <>
    <MDBContainer fluid className="min-vh-100 d-flex flex-column bg-muted-rose">
      <div className="d-flex flex-column flex-lg-row justify-content-center align-items-center flex-grow-1">
        {/* Image Section */}
        <div className="w-100 w-lg-50">
          <img
            src={heroImage}
            alt="Trading dashboard"
            className="img-fluid h-100 w-100 object-cover"
            style={{ objectFit: "cover", borderRadius: "1rem 0 0 1rem" }}
          />
        </div>

        {/* Form Section */}
        <div className="bg-white p-4 p-md-5 shadow-lg rounded w-100 w-lg-50">
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

            {/* Native select input styled to match */}
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
          </form>
        </div>
      </div>

      <Footer />
    </MDBContainer>

    <MDBToast
      open={showToast}
      setOpen={setShowToast}
      position="bottom-right"
      autohide
      delay={3500}
      color="success"
    >
      🎉 You're on the list! We'll be in touch soon.
    </MDBToast>
  </>
);

}

export default Login;
