// /frontend/src/pages/Landing.jsx
// Landing page for the project using MDB React

import React from "react";
import { Link } from "react-router-dom";
import "../styles/Landing.css";

const Landing = () => {
  return (
    <div className="landing-page">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="nav-container">
          <h1 className="brand">JedgeBot</h1>
          <ul className="nav-links">
            <li><Link to="/about">About</Link></li>
            <li><Link to="/pricing">Pricing</Link></li>
            <li><Link to="/how-it-works">How it Works</Link></li>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register" className="register-btn">Sign Up</Link></li>
          </ul>
        </div>
      </nav>
      
      {/* Hero Section as a Card */}
      <div className="hero-section">
        <div className="hero-card">
          <img src="/images/welcomejedgebot.webp" alt="JedgeBot" className="hero-image" />
          <h2>Welcome to JedgeBot</h2>
          <p>Your ultimate trading automation and portfolio management tool.</p>
          <div className="hero-buttons">
            <Link to="/login" className="btn btn-primary">Login</Link>
            <Link to="/register" className="btn btn-secondary">Sign Up</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
