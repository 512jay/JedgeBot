// /frontend/src/features/auth/ForgotPassword.jsx
import forgotImage from "@/images/hero/forgot.jpg";
// Page for requesting a password reset link, with a11y and semantic markup

import { MDBCardBody, MDBCol, MDBInput, MDBRow, MDBBtn } from "mdb-react-ui-kit";
import { Link } from "react-router-dom";

export default function ForgotPassword() {
  return (
    <div
      className="shadow-lg rounded-5 overflow-hidden bg-white mx-auto"
      style={{ maxWidth: "960px", width: "100%" }}
      role="main"
    >
      <MDBRow className="g-0">
        {/* Left image section */}
        <MDBCol md="6">
          <img
            src={forgotImage}
            alt="Reset password illustration"
            className="w-100 h-100 object-fit-cover"
          />
        </MDBCol>

        {/* Right form section */}
        <MDBCol md="6">
          <MDBCardBody
            className="d-flex flex-column justify-content-center p-5"
            aria-label="Password reset request form"
          >
            <h3 className="text-center mb-4">Forgot your password?</h3>
            <p className="text-center mb-4">
              Enter your email and we'll send you a reset link.
            </p>

            {/* Form input */}
            <form className="w-100" noValidate aria-label="Forgot password form">
              <label htmlFor="forgot-email" className="form-label">
                Email address
              </label>
              <MDBInput
                id="forgot-email"
                type="email"
                required
                size="lg"
                aria-label="Email address"
                className="mb-4"
              />

              {/* Submit button */}
              <MDBBtn
                type="submit"
                className="w-100 mb-3"
                color="primary"
                aria-label="Send password reset link"
              >
                Send Reset Link
              </MDBBtn>
            </form>

            {/* Navigation link */}
            <div className="text-center mt-2">
              <span>Remembered your password? </span>
              <Link to="/login" aria-label="Login page">
                Login
              </Link>
            </div>
          </MDBCardBody>
        </MDBCol>
      </MDBRow>
    </div>
  );
}
