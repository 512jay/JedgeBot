// /frontend/src/pages/Register.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { MDBInput, MDBBtn } from "mdb-react-ui-kit";
import { register } from "../api/auth_api";
import "../styles/global.css";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("free");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      await register({ email, password, role, username });
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
        <div className="auth-image">
          <img
            src="/images/registrationleft.jpg"
            alt="Confident Black woman in an upscale workspace"
          />
        </div>

        <div className="auth-box">
          <h2 className="text-center mb-4">Register</h2>
          {error && <p className="text-danger text-center">{error}</p>}

          <form onSubmit={handleRegister} className="w-100 px-4">
            <label htmlFor="role">Select Role</label>
            <select
              id="role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="mb-3 form-select"
            >
              <option value="free">Free – Manage 1 Brokerage Account</option>
              <option value="client">Client – $30/mo for 10 Brokerage Accounts</option>
              <option value="manager">Manager – $200/mo for 100 Brokerage Accounts</option>
            </select>

            <label htmlFor="username">Username</label>
            <MDBInput
              id="username"
              type="text"
              required
              value={username}
              autoComplete="username"
              onChange={(e) => setUsername(e.target.value)}
              className="mb-3"
            />
            <label htmlFor="email">Email Address</label>
            <MDBInput
              id="email"
              type="email"
              required
              value={email}
              autoComplete="email"
              onChange={(e) => setEmail(e.target.value)}
              className="mb-3"
            />

            <label htmlFor="password">Password</label>
            <MDBInput
              id="password"
              type="password"
              required
              value={password}
              autoComplete="new-password"
              onChange={(e) => setPassword(e.target.value)}
              className="mb-3"
            />

            <label htmlFor="confirm-password">Confirm Password</label>
            <MDBInput
              id="confirm-password"
              type="password"
              required
              value={confirmPassword}
              autoComplete="new-password"
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="mb-3"
            />

            <MDBBtn className="w-100" type="submit">
              Register
            </MDBBtn>
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
