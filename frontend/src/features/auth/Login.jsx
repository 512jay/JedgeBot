// /frontend/src/features/auth/Login.jsx
import React, { useState } from "react";
import {
  MDBContainer,
  MDBInput,
  MDBBtn,
  MDBTypography,
  MDBRow,
  MDBCol,
} from "mdb-react-ui-kit";
import { useNavigate } from "react-router-dom";
import { login } from "@auth/auth_api";

const loginImage = "/images/hero/login.webp";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (error) {
      console.error("Login failed", error);
      setErrorMsg("Login failed. Please check your credentials.");
    }
  };

  return (
    <main aria-label="Login Page">
      <MDBContainer fluid className="bg-muted-rose py-5">
        <MDBRow className="justify-content-center align-items-center min-vh-100">
          <MDBCol
            md="6"
            lg="5"
            className="d-none d-md-block p-0"
            style={{ borderRadius: "1rem 0 0 1rem", overflow: "hidden" }}
          >
            <img
              src={loginImage}
              alt="Person accessing a secure trading platform"
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </MDBCol>

          <MDBCol md="6" lg="5" className="p-4 d-flex align-items-center justify-content-center">
            <div
              className="bg-white p-4 shadow-lg rounded w-100"
              style={{ maxWidth: "400px" }}
              role="form"
              aria-labelledby="login-title"
            >
              <MDBTypography tag="h2" id="login-title" className="text-center fw-bold mb-4">
                Sign into your account
              </MDBTypography>

              <form onSubmit={handleLogin} noValidate>
                <label htmlFor="email" className="visually-hidden">
                  Email address
                </label>
                <MDBInput
                  id="email"
                  label="Email address"
                  type="email"
                  className="mb-3"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  aria-required="true"
                  autoComplete="email"
                />

                <label htmlFor="password" className="visually-hidden">
                  Password
                </label>
                <MDBInput
                  id="password"
                  label="Password"
                  type="password"
                  className="mb-3"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  aria-required="true"
                  autoComplete="current-password"
                />

                {errorMsg && (
                  <div
                    className="text-danger small mb-3"
                    role="alert"
                    aria-live="polite"
                  >
                    {errorMsg}
                  </div>
                )}

                <div className="text-end mb-3">
                  <a href="/forgot-password" className="small text-primary">
                    Forgot your password?
                  </a>
                </div>

                <MDBBtn
                  type="submit"
                  className="w-100 bg-primary"
                  aria-label="Submit login"
                >
                  LOGIN
                </MDBBtn>
              </form>

              <p className="mt-4 text-center">
                Don’t have an account?{" "}
                <a href="/register" className="text-primary">
                  Register here
                </a>
              </p>
            </div>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </main>
  );
}
