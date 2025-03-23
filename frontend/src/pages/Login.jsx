// /frontend/src/pages/Login.jsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { MDBInput, MDBBtn } from "mdb-react-ui-kit";
import { login } from "../api/auth_api";
import { useAuth } from "../context/AuthContext";
import { fetchUserProfile } from "@/api/auth_api";
import "../styles/global.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  //const { login: setUser } = useAuth();

  const handleLogin = async (e) => {
      e.preventDefault();
      setError(null); // Clear previous errors
      try {
          const response = await login(email, password);

          if (response.message === "Login successful") {
              console.log("✅ Login successful", response);
              navigate("/dashboard");
          } else {
              console.error("Login response error:", response);
              setError("Invalid credentials. Please try again.");
          }
      } catch (err) {
          console.error("Login error:", err);
          setError("Login failed. Please try again.");
      }
  };



  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-image">
          <img src="/images/leftlogin.jpg" alt="Professional Black woman with curly hair working on a laptop in a modern office." />
        </div>
        <div className="auth-box">
          <h2 className="text-center mb-4">Sign into your account</h2>
          {error && <p className="text-danger text-center">{error}</p>}
          <form onSubmit={handleLogin} className="w-100 px-4">
            <label htmlFor="email">Email Address</label>
            <MDBInput
              className="mb-3"
              label="Email address"
              type="email"
              id="email"
              name="email"
              required
              value={email}
              autoComplete="email"
              onChange={(e) => setEmail(e.target.value)}
            />

            <label htmlFor="password">Password</label>
            <MDBInput
              className="mb-2"
              label="Password"
              type="password"
              id="password"
              name="password"
              required
              value={password}
              autoComplete="current-password"
              onChange={(e) => setPassword(e.target.value)}
            />

            <div className="text-end mb-3">
              <a href="/forgot-password" className="text-muted" style={{ fontSize: "0.9rem" }}>
                Forgot your password?
              </a>

            </div>

            <MDBBtn className="auth-btn" type="submit">
              Login
            </MDBBtn>
          </form>

          <p className="mt-3 text-center">
            Don't have an account? <a href="/register" className="text-primary">Register here</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
