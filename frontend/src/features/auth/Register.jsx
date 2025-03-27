// /frontend/src/features/auth/Register.jsx
// Register component for user registration
import { Helmet } from "react-helmet-async";
import { MDBBtn, MDBInput, MDBTypography } from "mdb-react-ui-kit";
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "./auth_api";
import ToastMessage from '../../components/ToastMessage';


const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("free");
  const [error, setError] = useState(null);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);
  const navigate = useNavigate();

useEffect(() => {
  if (showToast) {
    const timer = setTimeout(() => {
      setShowToast(false);
      setToastMessage(null);
      navigate("/login"); // Move navigation here
    }, 3000);
    return () => clearTimeout(timer);
  }
}, [showToast, navigate]); // <-- include navigate as a dependency



  

  const handleRegister = async (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const response = await register({ email, password, role, username });
      setToastMessage(response?.message || "Registration successful! Please verify your account by email.");
      setShowToast(true);
      setTimeout(() => {
        setShowToast(false);
        navigate("/login");
      }, 3000);

    } catch (err) {
      console.error("Registration error:", err);
      setError("Registration failed. Please try again.");
    }
  };

  return (
    <div
      className="bg-mutedRose d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh", width: "100vw" }}
    >
      <ToastMessage
        show={showToast}
        message={toastMessage}
        type="success"
        onClose={() => {
          setShowToast(false);
          setToastMessage(null);
        }}
      />
      <Helmet>
        <title>Register | Fordis Ludus</title>
      </Helmet>
      <div
        className="shadow-lg rounded-5 overflow-hidden bg-white"
        style={{ maxWidth: "960px", width: "100%" }}
      >
        <div className="row g-0">
          {/* Left image */}
          <div className="col-md-6 d-none d-md-block">
            <img
              src="/images/registrationleft.jpg"
              alt="Confident Black woman in an upscale workspace"
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </div>

          {/* Right form */}
          <div className="col-md-6 d-flex flex-column justify-content-center align-items-center p-5">
            <MDBTypography tag="h4" className="mb-4">
              Register
            </MDBTypography>

            {error && <p className="text-danger text-center w-100 mb-3">{error}</p>}

            <form onSubmit={handleRegister} className="w-100 px-3">
              <label htmlFor="role" className="form-label">Select Role</label>
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

            <p className="text-center mt-4">
              Already have an account?{" "}
              <Link to="/login" className="text-primary">
                Login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
  
};

export default Register;
