// /frontend/src/features/auth/ResetPassword.jsx
import { useState, useEffect } from "react";
import {
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn,
} from "mdb-react-ui-kit";
import { toast } from "react-toastify";
import { useNavigate, useSearchParams } from "react-router-dom";
import fetchWithCredentials from "@/utils/fetchWithCredentials";

export default function ResetPassword() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      setError("Passwords do not match");
      return;
    }

    if (!token) {
      toast.error("Missing reset token.");
      setError("Missing reset token.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetchWithCredentials(
        `/auth/reset-password?token=${encodeURIComponent(token)}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ password }),
        }
      );

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data?.detail || "Failed to reset password.");
      }

      toast.success("Password reset! Redirecting to login...");
      setTimeout(() => navigate("/login"), 2500);
    } catch (err) {
      console.error("Reset error:", err);
      setError(err.message);
      toast.error(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <MDBContainer className="my-5">
      <MDBCard className="mx-auto" style={{ maxWidth: "500px" }}>
        <MDBCardBody className="p-5">
          <h4 className="mb-4 text-center">Reset Your Password</h4>
          {error && (
            <div className="alert alert-danger text-center mb-3">{error}</div>
          )}
          <form onSubmit={handleSubmit} noValidate>
            <MDBInput
              label="New Password"
              type="password"
              required
              className="mb-3"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <MDBInput
              label="Confirm New Password"
              type="password"
              required
              className="mb-3"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <MDBBtn type="submit" className="w-100" disabled={loading}>
              {loading ? "Resetting..." : "Reset Password"}
            </MDBBtn>
          </form>
        </MDBCardBody>
      </MDBCard>
    </MDBContainer>
  );
}
