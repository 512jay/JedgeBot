// /frontend/src/features/auth/ForgotPassword.jsx

import React, { useState } from "react";
import { MDBInput, MDBBtn, MDBTypography } from "mdb-react-ui-kit";
import { Helmet } from "react-helmet-async";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

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
      const response = await fetch(`${API_URL}/auth/forgot-password`, {
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
          {/* Left image */}
          <div className="col-md-6 d-none d-md-block">
            <img
              src="/images/registrationleft.jpg"
              alt="Forgot password visual"
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </div>

          {/* Right form */}
          <div className="col-md-6 d-flex flex-column justify-content-center align-items-center p-5">
            <MDBTypography tag="h4" className="mb-4 text-center">
              Forgot your password?
            </MDBTypography>

            <form onSubmit={handleSubmit} className="w-100 px-3">
              <label htmlFor="email" className="form-label">
                Enter your email address
              </label>
              <MDBInput
                className="mb-3"
                type="email"
                id="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              {error && <p className="text-danger text-center">{error}</p>}
              {message && <p className="text-success text-center">{message}</p>}

              <MDBBtn className="w-100" type="submit" disabled={loading}>
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
