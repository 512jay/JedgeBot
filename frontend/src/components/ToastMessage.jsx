// /frontend/src/features/auth/Register.jsx
// Handles user registration and displays toast messages upon success or failure.

import React, { useState, useEffect } from "react";
import {
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn,
  MDBTabs,
  MDBTabsItem,
  MDBTabsLink,
  MDBTabsContent,
  MDBTabsPane,
} from "mdb-react-ui-kit";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../../api/auth_api";
import ToastMessage from "../../components/ToastMessage";

export default function Register() {
  const navigate = useNavigate();

  const [justifyActive, setJustifyActive] = useState("tab1");
  const [form, setForm] = useState({
    email: "",
    password: "",
    username: "",
    role: "client",
  });

  const [toastMessage, setToastMessage] = useState(null);
  const [showToast, setShowToast] = useState(false);

  const handleJustifyClick = (value) => {
    if (value !== justifyActive) setJustifyActive(value);
  };

  const handleInputChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await registerUser(form);
      if (response.status === 200) {
        setToastMessage("Registration successful. Please verify your account by email.");
        setShowToast(true);
        setForm({ email: "", password: "", username: "", role: "client" });
      } else {
        throw new Error("Unexpected error occurred.");
      }
    } catch (error) {
      setToastMessage(error.response?.data?.detail || "Registration failed.");
      setShowToast(true);
    }
  };

  useEffect(() => {
    if (showToast) {
      const timer = setTimeout(() => {
        setShowToast(false);
        setToastMessage(null);
      }, 6000);
      return () => clearTimeout(timer);
    }
  }, [showToast]);

  return (
    <MDBContainer fluid className="d-flex justify-content-center align-items-center vh-100" style={{ backgroundColor: "#9A616D" }}>
      <MDBCard className="text-black m-5" style={{ maxWidth: "500px", width: "100%" }}>
        <MDBCardBody>
          <MDBTabs pills justify className="mb-3 d-flex flex-row justify-content-between">
            <MDBTabsItem>
              <MDBTabsLink onClick={() => handleJustifyClick("tab1")} active={justifyActive === "tab1"}>
                Register
              </MDBTabsLink>
            </MDBTabsItem>
            <MDBTabsItem>
              <MDBTabsLink onClick={() => navigate("/login")} active={justifyActive === "tab2"}>
                Login
              </MDBTabsLink>
            </MDBTabsItem>
          </MDBTabs>

          <MDBTabsContent>
            <MDBTabsPane show={justifyActive === "tab1"}>
              <form onSubmit={handleSubmit}>
                <MDBInput
                  wrapperClass="mb-4"
                  label="Email"
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={handleInputChange}
                  required
                />
                <MDBInput
                  wrapperClass="mb-4"
                  label="Password"
                  name="password"
                  type="password"
                  value={form.password}
                  onChange={handleInputChange}
                  required
                />
                <MDBInput
                  wrapperClass="mb-4"
                  label="Username"
                  name="username"
                  type="text"
                  value={form.username}
                  onChange={handleInputChange}
                  required
                />
                <MDBBtn type="submit" className="mb-4 w-100">Register</MDBBtn>
              </form>
            </MDBTabsPane>
          </MDBTabsContent>
        </MDBCardBody>
      </MDBCard>

      <ToastMessage
        show={showToast}
        message={toastMessage}
        type="success"
        onClose={() => {
          setShowToast(false);
          setToastMessage(null);
        }}
      />
    </MDBContainer>
  );
}
