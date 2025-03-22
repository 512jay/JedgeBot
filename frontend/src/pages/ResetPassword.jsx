// /frontend/src/pages/ResetPassword.jsx

import React, { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { MDBInput, MDBBtn } from "mdb-react-ui-kit";
import "../styles/global.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const [password, setPassword] = useState("");
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      setError("Reset token missing.");
      setLoading(false);
      return;
    }

    const checkToken = async () => {
      try {
        const res = await fetch(`${API_URL}/auth/validate-token?token=${token}`);
        if (!res.ok) {
          const data = await res.json();
          setError(data.detail || "Token is invalid or expired.");
        }
      } catch (err) {
        console.error("Token validation error:", err);
        setError("Could not validate token.");
      } finally {
        setLoading(false);
      }
    };

    checkToken();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await fetch(`${API_URL}/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, new_password: password }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => navigate("/login"), 3000);
      } else {
        setError(data.detail || "Reset failed.");
      }
    } catch (err) {
      console.error("Reset error:", err);
      setError("Something went wrong.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-image">
          <img src="/images/registrationleft.jpg" alt="Reset password visual" />
        </div>
        <div className="auth-box">
          <h2 className="text-center mb-4">Reset Your Password</h2>

          {loading ? (
            <p className="text-center">🔄 Checking your reset link...</p>
          ) : error ? (
            <p className="text-danger text-center">{error}</p>
          ) : success ? (
            <p className="text-success text-center">
              ✅ Password reset. Redirecting to login...
            </p>
          ) : (
            <form onSubmit={handleSubmit} className="w-100 px-4">
              <label htmlFor="password">New Password</label>
              <MDBInput
                className="mb-3"
                type="password"
                id="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <MDBBtn className="auth-btn" type="submit">
                Reset Password
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

export default ResetPassword;
