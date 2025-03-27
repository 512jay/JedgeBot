// /frontend/src/features/auth/VerifyEmail.jsx
import React, { useEffect, useState } from "react";
import { MDBTypography, MDBBtn } from "mdb-react-ui-kit";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";

const API_URL = import.meta.env.VITE_API_URL;

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const [status, setStatus] = useState("loading"); // loading, success, error
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Missing or invalid token.");
      return;
    }

    fetch(`${API_URL}/auth/verify-email?token=${token}`, {
      method: "GET",
      credentials: "include",
    })
      .then(async (res) => {
        if (res.ok) {
          setStatus("success");
          setMessage("✅ Email verified! Redirecting to login...");
          setTimeout(() => navigate("/login?verified=true"), 3000);
        } else {
          const data = await res.json();
          setStatus("error");
          setMessage(data.detail || "Verification failed.");
        }
      })
      .catch(() => {
        setStatus("error");
        setMessage("Something went wrong while verifying your email.");
      });
  }, [token, navigate]);

  return (
    <div
      className="bg-mutedRose d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh", width: "100vw" }}
    >
      <Helmet>
        <title>Verify Email | JedgeBot</title>
      </Helmet>

      <div
        className="shadow-lg rounded-5 overflow-hidden bg-white p-5 text-center"
        style={{ maxWidth: "500px", width: "100%" }}
      >
        <MDBTypography tag="h4" className="mb-4">
          Email Verification
        </MDBTypography>

        <p className={`text-${status === "success" ? "success" : "danger"}`}>
          {message}
        </p>

        {status === "error" && (
          <MDBBtn color="primary" onClick={() => navigate("/login")}>
            ← Back to Login
          </MDBBtn>
        )}
      </div>
    </div>
  );
}
