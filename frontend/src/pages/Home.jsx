import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/global.css"; // Use global styles

function Home() {
  const navigate = useNavigate();

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Left Image Section */}
        <div className="auth-image">
          <img
            src="/images/welcomejedgebot.jpg"
            alt="Professional trading workspace with financial charts and business elements, representing JedgeBot's smart trading solutions."
          />
        </div>
        
        {/* Right Content Section */}
        <div className="auth-box">
          <h1>Fordis Ludus</h1>
          <p>Manage your trading strategies with ease.</p>
          <button className="btn btn-primary" onClick={() => navigate("/login")}>
            ENTER
          </button>
        </div>
      </div>
    </div>
  );
}

export default Home;
