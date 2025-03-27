// /frontend/src/features/auth/Login.jsx

import { Helmet } from "react-helmet-async";
import React, { useState } from "react";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBInput,
  MDBBtn,
  MDBTypography
} from "mdb-react-ui-kit";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { login } from "./auth_api";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { setUser } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
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

        if (
          typeof message === "string" &&
          message.toLowerCase().includes("email not verified")
        ) {
          setError(
            "Your email address has not been verified. Please check your inbox for the verification email."
          );
        } else {
          setError(message);
        }
      }
  };

  const handleResendVerification = async () => {
    try {
      const res = await fetch(`${API_URL}/auth/resend-verification`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();
      setError(data.message || "Verification email resent.");
    } catch (err) {
      setError("Failed to resend verification email. Please try again.");
    }
  };

  return (
    <div
      className="bg-mutedRose d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh", width: "100vw" }}
    >
      <Helmet>
        <title>Login | Fordis Ludus</title>
      </Helmet>
      <div
        className="shadow-lg rounded-5 overflow-hidden bg-white"
        style={{ maxWidth: "960px", width: "100%" }}
      >
        <MDBRow className="g-0">
          {/* Left side image */}
          <MDBCol md="6" className="d-none d-md-block">
            <img
              src="/images/leftlogin.jpg"
              alt="Professional Black woman working on a laptop"
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </MDBCol>

          {/* Right side form */}
          <MDBCol
            md="6"
            className="d-flex flex-column justify-content-center align-items-center p-5"
          >
            <MDBTypography tag="h4" className="mb-4">
              Sign into your account
            </MDBTypography>

            {error && (
              <>
                <p className="text-danger text-center w-100 mb-2">{error}</p>
                {error.toLowerCase().includes("not been verified") && (
                  <div className="text-center mb-3">
                    <MDBBtn
                      color="warning"
                      size="sm"
                      onClick={handleResendVerification}
                    >
                      Resend Verification Email
                    </MDBBtn>
                  </div>
                )}
              </>
            )}


            <form onSubmit={handleLogin} className="w-100 px-3">
              <label htmlFor="email" className="form-label">
                Email Address
              </label>
              <MDBInput
                id="email"
                type="email"
                required
                value={email}
                autoComplete="email"
                className="mb-3"
                onChange={(e) => setEmail(e.target.value)}
              />

              <label htmlFor="password" className="form-label">
                Password
              </label>
              <MDBInput
                id="password"
                type="password"
                required
                value={password}
                autoComplete="current-password"
                className="mb-2"
                onChange={(e) => setPassword(e.target.value)}
              />

              <div className="text-end mb-3">
                <a
                  href="/forgot-password"
                  className="text-muted"
                  style={{ fontSize: "0.9rem" }}
                >
                  Forgot your password?
                </a>
              </div>

              <MDBBtn className="w-100" type="submit">
                LOGIN
              </MDBBtn>
            </form>

            <p className="mt-4 text-center">
              Don't have an account?{" "}
              <a href="/register" className="text-primary">
                Register here
              </a>
            </p>
          </MDBCol>
        </MDBRow>
      </div>
    </div>
  );
}


export default Login;
