// /frontend/src/features/auth/VerifyEmail.jsx
// Handles email verification from token link in email

import { useEffect, useState, useRef } from "react";
import { useSearchParams, Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { config } from "@/config";

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  const [status, setStatus] = useState("verifying"); // verifying | missing | success | error
  const hasRun = useRef(false); // Prevent double call in dev

  useEffect(() => {
    if (!token) {
      setStatus("missing");
      return;
    }

    if (hasRun.current) return;
    hasRun.current = true;

    const verify = async () => {
      try {
        const res = await fetch(`${config.API_URL}/auth/verify-email?token=${token}`, {
          method: "GET",
          credentials: "include",
        });

        if (!res.ok) {
          const data = await res.json();
          throw new Error(data?.detail || "Verification failed");
        }

        toast.success("Email verified. You can now log in.");
        setStatus("success");

        setTimeout(() => navigate("/login"), 3000);
      } catch (err) {
        console.error("Email verification error:", err);
        toast.error("Verification failed. Please try again.");
        setStatus("error");
      }
    };

    verify();
  }, [token, navigate]);

  return (
    <div className="container py-5">
      {status === "verifying" && (
        <div className="text-center">
          <h3>Verifying your email...</h3>
        </div>
      )}

      {status === "missing" && (
        <div className="text-center text-danger">
          <h4>Missing or invalid token.</h4>
        </div>
      )}

      {status === "success" && (
        <div className="text-center text-success">
          <h4>Email verified successfully!</h4>
          <p>Redirecting to login...</p>
        </div>
      )}

      {status === "error" && (
        <div className="text-center text-danger">
          <h4>Verification failed.</h4>
          <p>
            <Link to="/resend-verification" className="text-decoration-underline">
              Try again
            </Link>
          </p>
        </div>
      )}
    </div>
  );
}
