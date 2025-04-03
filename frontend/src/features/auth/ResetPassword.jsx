// /frontend/src/features/auth/ResetPassword.jsx
import { useState } from "react";
import { MDBContainer, MDBCard, MDBCardBody, MDBInput, MDBBtn } from "mdb-react-ui-kit";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { resetPassword } from "@auth/auth_api"; // Adjust the import if necessary

export default function ResetPassword() {
  const [email, setEmail] = useState(""); // Or if you need a token field, add that too
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      toast.error("Passwords do not match");
      return;
    }

    try {
      setLoading(true);

      const response = await resetPassword({
        email, // if needed
        password,
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || "Reset password failed");
      }

      toast.success("Password reset successful! Redirecting to login...");
      // Optionally, clear form fields here
      setTimeout(() => navigate("/login"), 3000);
    } catch (err) {
      console.error("Reset password error:", err);
      setError(err.message);
      toast.error(err.message || "Reset password failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <MDBContainer className="my-5">
      <MDBCard className="mx-auto" style={{ maxWidth: "500px" }}>
        <MDBCardBody className="p-5">
          <h4 className="mb-4 text-center">Reset Your Password</h4>
          {error && <div className="alert alert-danger text-center mb-3">{error}</div>}
          <form onSubmit={handleSubmit} noValidate>
            <MDBInput
              label="Email address"
              type="email"
              required
              className="mb-3"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
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
