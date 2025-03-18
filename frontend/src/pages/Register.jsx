import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth";
import "../styles/global.css"; // Import global styles

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords do not match!");
      return;
    }
    try {
      const data = await register(email, password);
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        setSuccess("Registration successful! Redirecting to dashboard...");
        setTimeout(() => navigate("/dashboard"), 2000);
      } else {
        throw new Error("Registration failed!");
      }
    } catch {
      setError("Registration failed! Please try again.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Left Image */}
        <div className="auth-image">
          <img src="/images/registrationleft.jpg" alt="A luxurious and inspiring image of a confident Black woman in an upscale workspace." />
        </div>
        
        {/* Right Registration Form */}
        <div className="auth-box">
          <h2 className="text-center mb-4">Register</h2>
          {error && <p className="text-danger text-center">{error}</p>}
          {success && <p className="text-success text-center">{success}</p>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-control mb-3"
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-control mb-3"
              required
            />
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="form-control mb-3"
              required
            />
            <button type="submit" className="btn btn-primary w-100">Register</button>
          </form>
          <p className="text-center mt-3">
            Already have an account? <a href="/login" className="text-primary">Login</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;