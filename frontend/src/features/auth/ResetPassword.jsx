// /frontend/src/features/auth/ResetPassword.jsx
import registrationleftImage from "@/images/registrationleft.jpg";
// Handles user password reset with token validation, a11y support, and feedback UI

import React, { useState, useEffect } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import { MDBInput, MDBBtn, MDBTypography } from "mdb-react-ui-kit";
import { toast } from 'react-toastify';

const API_URL = import.meta.env.VITE_API_URL;

function ResetPassword({ handleSuccess }) {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const navigate = useNavigate();

  // State management
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tokenValid, setTokenValid] = useState(false);

  const handleSuccessFn = handleSuccess || ((cb) => setTimeout(cb, 3000));

  // Validate reset token on mount
  useEffect(() => {
    if (!token) {
      setError("Reset token missing.");
      toast.error("Reset token missing.")
      setLoading(false);
      return;
    }

    const checkToken = async () => {
      try {
        const res = await fetch(`${API_URL}/auth/validate-token?token=${token}`);
        if (!res.ok) {
          const data = await res.json();
          setError(data.detail || "Token is invalid or expired.");
        } else {
          setTokenValid(true);
        }
      } catch (err) {
        console.error("Token validation error:", err);
        setError("Could not validate token.");
        toast.error("Could not validate token.");
      } finally {
        setLoading(false);
      }
    };

    checkToken();
  }, [token]);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      toast.error("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, new_password: password }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        handleSuccessFn(() => navigate("/login"));
      } else {
        setError(data.detail || "Reset failed.");
        toast.error(data.detail || "Reset failed.");
      }
    } catch (err) {
      console.error("Reset error:", err);
      setError("Something went wrong.");
      toast.error("Something went wrong.");
    }
  };

  return (
    <div
      className="bg-mutedRose d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh", width: "100vw" }}
    >

      <div
        className="shadow-lg rounded-5 overflow-hidden bg-white"
        style={{ maxWidth: "960px", width: "100%" }}
        role="main"
      >
        <div className="row g-0">
          {/* Left image panel */}
          <div className="col-md-6 d-none d-md-block">
            <img
              src={registrationleftImage}
              alt="Reset password visual"
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </div>

          {/* Right form panel */}
          <div className="col-md-6 d-flex flex-column justify-content-center align-items-center p-5 position-relative">
            <MDBTypography tag="h4" className="mb-4 text-center">
              Reset Your Password
            </MDBTypography>


            {/* Feedback area for screen readers */}
            <div aria-live="polite" className="w-100 text-center">
              {loading && <p>🔄 Checking your reset link...</p>}
              {success && (
                <p className="text-success" role="alert">
                  ✅ Password reset. Redirecting to login...
                </p>
              )}
              {error && !loading && (
                <p className="text-danger mb-3" role="alert">
                  {error}
                </p>
              )}
            </div>

            {/* Password reset form */}
            {!loading && tokenValid && !success && (
              <form onSubmit={handleSubmit} className="w-100 px-3" aria-label="Reset password form">
                <label htmlFor="password" className="form-label">
                  New Password
                </label>
                <MDBInput
                  id="password"
                  type="password"
                  required
                  autoComplete="new-password"
                  className="mb-3"
                  aria-required="true"
                  aria-label="New password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />

                <label htmlFor="confirmPassword" className="form-label">
                  Confirm Password
                </label>
                <MDBInput
                  id="confirmPassword"
                  type="password"
                  required
                  autoComplete="new-password"
                  className="mb-3"
                  aria-required="true"
                  aria-label="Confirm password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />

                <MDBBtn type="submit" className="w-100" aria-label="Submit new password">
                  Reset Password
                </MDBBtn>
              </form>
            )}

            {/* Expired token message */}
            {!loading && !tokenValid && (
              <p className="text-danger text-center" role="alert">
                This password reset link is invalid or expired.
              </p>
            )}

            {/* Back to login link */}
            <p className="mt-4 text-center">
              <Link to="/login" className="text-primary" aria-label="Back to login">
                ← Back to login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResetPassword;
