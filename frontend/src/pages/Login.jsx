// /frontend/src/pages/Login.jsx

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { MDBInput, MDBBtn } from "mdb-react-ui-kit";
import { login } from "../api/api";
import "../styles/global.css"; // Import global styles

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await login(email, password);
      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
        console.log("Token stored:", localStorage.getItem("access_token")); // Debugging line
        navigate("/dashboard");
      } else {
        setError("Invalid email or password");
      }
    } catch (err) {
      console.error("Login error:", err); // Added error logging
      setError("Login failed. Please try again.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Left Image */}
        <div className="auth-image">
          <img src="/images/leftlogin.jpg" alt="Professional Black woman with curly hair working on a laptop in a modern office." />
        </div>

        {/* Right Login Form */}
        <div className="auth-box">
          <h2 className="text-center mb-4">Sign into your account</h2>
          {error && <p className="text-danger text-center">{error}</p>}
          <form onSubmit={handleSubmit} className="w-100 px-4">
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
              className="mb-3"
              label="Password"
              type="password"
              id="password"
              name="password"
              required
              value={password}
              autoComplete="current-password"
              onChange={(e) => setPassword(e.target.value)}
            />


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
