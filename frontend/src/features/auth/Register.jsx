// /frontend/src/features/auth/Register.jsx
// Registration form for new users with validation, feedback, and role selection.

import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { MDBInput, MDBBtn } from "mdb-react-ui-kit";
import { register } from "@auth/auth_api";
import ToastMessage from "@/components/common/ToastMessage";

const roleOptions = [
  { value: "free", label: "Free – Manage 1 Brokerage Account" },
  { value: "client", label: "Client – $30/mo for 10 Brokerage Accounts" },
  { value: "manager", label: "Manager – $200/mo for 100 Brokerage Accounts" },
];

export default function Register(props) {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("free");
  const [error, setError] = useState(null);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const internalNavigate = useNavigate();
  const navigateFn = props?.navigateFn || internalNavigate;
  const usernameRef = useRef(null);
  const handleSuccessFn = props?.handleSuccess || handleSuccess;

  useEffect(() => {
    usernameRef.current?.focus();
  }, []);

  function handleSuccess(navigateCallback) {
    setTimeout(navigateCallback, 2000);
  }


  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    try {
      const result = await register(email, password, username, role);
      if (result?.message === "Registration successful") {
        setToastMessage("Registration successful. Please verify your email.");
        setShowToast(true);
        handleSuccessFn(() => navigateFn("/login"));
      } else {
        setError("Something went wrong. Please try again.");
      }
    } catch (err) {
      const message =
        err?.response?.data?.detail || err?.message || "Registration failed.";
      setError(message);
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center bg-mutedRose" style={{ minHeight: "100vh", width: "100vw" }}>
      <div className="shadow-lg rounded-5 overflow-hidden bg-white" style={{ maxWidth: "960px", width: "100%" }}>
        <div className="row g-0">
          <div className="col-md-6 d-none d-md-block">
            <img
              src="/images/registrationleft.jpg"
              alt="Confident Black woman in a professional setting, seated at a modern desk in a stylish office, wearing a beige blazer and natural hair styled in an afro."
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover" }}
            />
          </div>

          <div className="col-md-6 p-5 d-flex flex-column justify-content-center align-items-center">
            <h4 className="mb-4">Create your account</h4>

            <form className="w-100 px-3" onSubmit={handleRegister} noValidate>
              <MDBInput
                label="Email Address"
                aria-label="Email Address"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mb-3"
                required
                autoComplete="email"
              />

              <MDBInput
                label="Username"
                aria-label="Username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="mb-3"
                required
                autoComplete="username"
                ref={usernameRef}
              />

              <MDBInput
                label="Password"
                aria-label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mb-3"
                required
                autoComplete="new-password"
              />

              <MDBInput
                label="Confirm Password"
                aria-label="Confirm Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="mb-3"
                required
                autoComplete="new-password"
              />

              <label htmlFor="role" className="form-label">
                Choose your role:
              </label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="mb-3 form-select"
                aria-label="Choose your role"
              >
                {roleOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              {error && (
                <div className="alert alert-danger text-center w-100 mb-3" role="alert" data-testid="registration-error">
                  {error}
                </div>
              )}

              <MDBBtn className="w-100" type="submit" data-testid="register-btn">
                Register
              </MDBBtn>
            </form>

            <MDBBtn className="mt-3" onClick={() => navigateFn("/login")} data-testid="go-login-btn">
              Go to Login
            </MDBBtn>

            <ToastMessage
              showToast={showToast}
              setShowToast={setShowToast}
              message={toastMessage}
              color="success"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
