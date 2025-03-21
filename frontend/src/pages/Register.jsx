import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth_api";
import "../styles/global.css";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      await register({ email, password });
      alert("Registration successful! Please log in.");
      navigate("/login");
    } catch (err) {
      console.error("Registration error:", err);
      setError("Registration failed. Please try again.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Left Image */}
        <div className="auth-image">
          <img
            src="/images/registrationleft.jpg"
            alt="Confident Black woman in an upscale workspace"
          />
        </div>

        {/* Right Form */}
        <div className="auth-box">
          <h2 className="text-center mb-4">Register</h2>
          {error && <p className="text-danger text-center">{error}</p>}

          <form onSubmit={handleRegister}>
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              required
              autoComplete="email"
              onChange={(e) => setEmail(e.target.value)}
              className="form-control mb-3"
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              required
              autoComplete="new-password"
              onChange={(e) => setPassword(e.target.value)}
              className="form-control mb-3"
            />

            <label htmlFor="confirm-password">Confirm Password</label>
            <input
              id="confirm-password"
              type="password"
              value={confirmPassword}
              required
              autoComplete="new-password"
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="form-control mb-3"
            />

            <button type="submit" className="btn btn-primary w-100">
              Register
            </button>
          </form>

          <p className="text-center mt-3">
            Already have an account?{" "}
            <a href="/login" className="text-primary">
              Login
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
