// /frontend/src/features/auth/ResetPassword.jsx
import React, { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { MDBInput, MDBBtn, MDBTypography } from "mdb-react-ui-kit";
import { Helmet } from "react-helmet-async";

const API_URL = import.meta.env.VITE_API_URL;

function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const navigate = useNavigate();
  const handleSuccessFn = props?.handleSuccess || ((cb) => setTimeout(cb, 3000));

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tokenValid, setTokenValid] = useState(false);

      
            
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
      } else {
        setTokenValid(true);
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

    if (password !== confirmPassword) {
      triggerToast("Passwords do not match.");
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
      }
    } catch (err) {
      console.error("Reset error:", err);
      setError("Something went wrong.");
    }
  
  return (
    <div
      className="bg-mutedRose d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh", width: "100vw" }}
    >
      <Helmet>
        <title>Reset Password | JedgeBot</title>
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
              alt="Reset password visual"
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </div>

          {/* Right form */}
          <div className="col-md-6 d-flex flex-column justify-content-center align-items-center p-5 position-relative">
            <MDBTypography tag="h4" className="mb-4 text-center">
              Reset Your Password
            </MDBTypography>

            {/* Toast */}
                        <ToastMessage showToast={!!error} setShowToast={() => setError(null)} message={error} color="danger" />

                  ></button>
                </div>
              </div>
            )}

            {loading ? (
              <p className="text-center">🔄 Checking your reset link...</p>
            ) : success ? (
              <p className="text-success text-center">
                ✅ Password reset. Redirecting to login...
              </p>
            ) : tokenValid ? (
              <>
                {error && <p className="text-danger text-center mb-3">{error}</p>}
                <form onSubmit={handleSubmit} className="w-100 px-3">
                  <label htmlFor="password" className="form-label">
                    New Password
                  </label>
                  <MDBInput
                    className="mb-3"
                    type="password"
                    id="password"
                    required
                    value={password}
                    autoComplete="new-password"
                    onChange={(e) => setPassword(e.target.value)}
                  />

                  <label htmlFor="confirmPassword" className="form-label">
                    Confirm Password
                  </label>
                  <MDBInput
                    className="mb-3"
                    type="password"
                    id="confirmPassword"
                    required
                    value={confirmPassword}
                    autoComplete="new-password"
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />

                  <MDBBtn className="w-100" type="submit">
                    Reset Password
                  </MDBBtn>
                </form>
              </>
            ) : (
              <>
                <p className="text-danger text-center">
                  This password reset link is invalid or expired.
                </p>
              </>
            )}

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

export default ResetPassword;
