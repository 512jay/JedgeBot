// /frontend/src/features/auth/ResendVerification.jsx
import { useState } from "react";
import { MDBCardBody, MDBCol, MDBInput, MDBRow, MDBBtn } from "mdb-react-ui-kit";
import { Link } from "react-router-dom";
import forgotImage from "@/images/hero/forgot.jpg";
import fetchWithCredentials from "@/utils/fetchWithCredentials";

export default function ResendVerification() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setErrorMsg("");

    try {
      const res = await fetchWithCredentials("/auth/resend-verification", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });
      

      if (!res.ok) {
        throw new Error((await res.json()).detail || "Request failed");
      }

      const data = await res.json();
      setMessage(data.message || "Verification email sent.");
    } catch (err) {
      console.error("Resend verification failed", err);
      setErrorMsg(err.message || "Something went wrong.");
    }
  };

  return (
    <div
      className="shadow-lg rounded-5 overflow-hidden bg-white mx-auto"
      style={{ maxWidth: "960px", width: "100%" }}
      role="main"
    >
      <MDBRow className="g-0">
        <MDBCol md="6">
          <img
            src={forgotImage}
            alt="Email verification illustration"
            className="w-100 h-100 object-fit-cover"
          />
        </MDBCol>

        <MDBCol md="6">
          <MDBCardBody className="d-flex flex-column justify-content-center p-5">
            <h3 className="text-center mb-4">Verify your email.</h3>
            <p className="text-center mb-4">
              Enter your email and we’ll resend the verification link.
            </p>

            <form className="w-100" onSubmit={handleSubmit} noValidate>
              <label htmlFor="verify-email" className="form-label">
                Email address
              </label>
              <MDBInput
                id="verify-email"
                type="email"
                required
                size="lg"
                className="mb-4"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <MDBBtn type="submit" className="w-100 mb-3" color="primary">
                Resend Verification Email
              </MDBBtn>
            </form>

            {message && <p className="text-success text-center">{message}</p>}
            {errorMsg && <p className="text-danger text-center">{errorMsg}</p>}

            <div className="text-center mt-2">
              <span>Already verified? </span>
              <Link to="/login">Login</Link>
            </div>
          </MDBCardBody>
        </MDBCol>
      </MDBRow>
    </div>
  );
}
