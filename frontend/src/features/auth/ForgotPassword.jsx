// /frontend/src/features/auth/ForgotPassword.jsx
import React, { useState, useEffect } from "react";
import {
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn,
} from "mdb-react-ui-kit";
import { toast } from "react-toastify";
import { useSearchParams } from "react-router-dom";
import { fetchWithCredentials } from "@/utils/fetchWithCredentials";

export default function ForgotPassword() {
  const [searchParams] = useSearchParams();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const emailFromQuery = searchParams.get("email");
    if (emailFromQuery) setEmail(emailFromQuery);
  }, [searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      toast.error("Please enter your email.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetchWithCredentials("/auth/request-password-reset", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data?.detail || "Failed to send reset email.");
      }

      toast.success("Reset link sent! Please check your email.");
    } catch (err) {
      console.error(err);
      toast.error(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <MDBContainer className="my-5">
      <MDBCard className="mx-auto" style={{ maxWidth: "500px" }}>
        <MDBCardBody className="p-5">
          <h4 className="mb-4 text-center">Forgot Your Password?</h4>
          <form onSubmit={handleSubmit} noValidate>
            <MDBInput
              label="Email address"
              type="email"
              className="mb-4"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <MDBBtn type="submit" className="w-100" disabled={loading}>
              {loading ? "Sending..." : "Send Reset Link"}
            </MDBBtn>
          </form>
        </MDBCardBody>
      </MDBCard>
    </MDBContainer>
  );
}
