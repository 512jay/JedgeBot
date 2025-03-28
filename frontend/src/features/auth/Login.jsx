// /frontend/src/features/auth/Login.jsx
import React, { useState } from "react";
import {
  MDBBtn,
  MDBCardBody,
  MDBCol,
  MDBInput,
  MDBRow,
} from "mdb-react-ui-kit";
import { useNavigate } from "react-router-dom";
import { login } from "@auth/auth_api";
import loginImage from "@images/hero/login.webp"; // keep consistent with register

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
    <div
      className="shadow-lg rounded-5 overflow-hidden bg-white mx-auto"
      style={{ maxWidth: "960px", width: "100%" }}
    >
      <MDBRow className="g-0">
        <MDBCol md="6">
          <img
            src={loginImage}
            alt="Secure login to trading platform"
            className="w-100 h-100 object-fit-cover"
          />
        </MDBCol>

        <MDBCol md="6">
          <MDBCardBody
            className="d-flex flex-column justify-content-center p-5"
            aria-labelledby="login-title"
          >
            <h3 id="login-title" className="text-center mb-4">
              Sign into your account
            </h3>

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
          </MDBCardBody>
        </MDBCol>
      </MDBRow>
    </div>
  );
}
