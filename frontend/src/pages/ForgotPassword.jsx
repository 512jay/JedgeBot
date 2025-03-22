// /frontend/src/pages/ForgotPassword.jsx

import React, { useState } from "react";
import { MDBInput, MDBBtn } from "mdb-react-ui-kit";
import "../styles/global.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await fetch(`${API_URL}/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        setSubmitted(true);
      } else {
        const data = await response.json();
        setError(data.detail || "Something went wrong.");
      }
    } catch (err) {
      console.error("Forgot password error:", err);
      setError("Failed to send reset request.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-image">
          <img src="/images/registrationleft.jpg" alt="Password recovery illustration" />
        </div>
        <div className="auth-box">
          <h2 className="text-center mb-4">Forgot your password?</h2>

          {submitted ? (
            <p className="text-success text-center">
              If that email exists, a reset link has been sent.
            </p>
          ) : (
            <form onSubmit={handleSubmit} className="w-100 px-4">
              <label htmlFor="email">Enter your email address</label>
              <MDBInput
                className="mb-3"
                type="email"
                id="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              {error && <p className="text-danger text-center">{error}</p>}

              <MDBBtn className="auth-btn" type="submit">
                Request Reset Link
              </MDBBtn>
            </form>
          )}

          <p className="mt-3 text-center">
            <a href="/login" className="text-primary">Back to login</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default ForgotPassword;
//             Don't have an account?{" "}
//             <a href="/register" className="text-primary">Register here</a>       
