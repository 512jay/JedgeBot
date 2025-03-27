// /frontend/src/features/auth/ForgotPassword.jsx
// Forgot password form allowing users to request a reset email.

import React, { useState } from "react";
import { MDBInput, MDBBtn, MDBTypography } from "mdb-react-ui-kit";
import { Helmet } from "react-helmet-async";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const RESET_ENDPOINT = `${API_URL}/auth/forgot-password`;

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    try {
      const response = await fetch(RESET_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`If an account exists for ${email}, a reset link has been sent.`);
      } else {
        setError(data.detail || "Something went wrong.");
      }
    } catch (err) {
      console.error("Forgot password error:", err);
      setError("Unable to process your request. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="bg-mutedRose d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh", width: "100vw" }}
    >
      <Helmet>
        <title>Forgot Password | FL</title>
      </Helmet>

      <div
        className="shadow-lg rounded-5 overflow-hidden bg-white"
        style={{ maxWidth: "960px", width: "100%" }}
      >
        <div className="row g-0">
          {/* Left Image */}
          <div className="col-md-6 d-none d-md-block">
            <img
              src="/images/registrationleft.jpg"
              alt="Confident Black woman in a professional setting, seated at a modern desk in a stylish office, wearing a beige blazer and natural hair styled in an afro."
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </div>

          {/* Right Form */}
          <div className="col-md-6 d-flex flex-column justify-content-center align-items-center p-5">
            <MDBTypography tag="h4" className="mb-4 text-center">
              Forgot your password?
            </MDBTypography>

            <form onSubmit={handleSubmit} className="w-100 px-3" noValidate>
              <label htmlFor="email" className="form-label">
                Enter your email address
              </label>
              <MDBInput
                id="email"
                type="email"
                required
                autoComplete="email"
                className="mb-3"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                aria-describedby="forgot-help-text"
              />

              {error && <p className="text-danger text-center" role="alert">{error}</p>}
              {message && <p className="text-success text-center" role="status">{message}</p>}

              <MDBBtn type="submit" className="w-100" disabled={loading}>
                {loading ? "Sending..." : "Request Reset Link"}
              </MDBBtn>
            </form>

            <p className="mt-4 text-center">
              <a href="/login" className="text-primary">
                ← Back to login
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ForgotPassword;
