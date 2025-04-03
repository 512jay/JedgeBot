import { useState } from "react";
import {
  MDBInput,
  MDBBtn,
  MDBValidation,
  MDBValidationItem,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
} from "mdb-react-ui-kit";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { login } from "@auth/auth_api";
import { useAuth } from "@hooks/useAuth";
import loginImage from "@/images/hero/login.jpg";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();
  const { checkAuth } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      await login(email, password);
      console.log("🔁 Calling checkAuth() in Login.jsx");
      await checkAuth();
      toast.success("Login successful!");
      navigate("/dashboard");
    } catch (error) {
      console.error("Login failed", error);
      const detail = error?.response?.data?.detail;

      if (detail === "Email not verified") {
        setErrorMsg(
          <>
            Your email is not verified.{" "}
            <Link to="/resend-verification" className="text-decoration-underline">
              Resend verification email
            </Link>
          </>
        );
      } else {
        setErrorMsg("Login failed. Please check your credentials.");
      }

      toast.error("Login failed. Check credentials or verify your email.");
    }
  };

  return (
    <MDBContainer className="my-5">
      <MDBCard>
        <MDBRow className="g-0">
          <MDBCol md="6" className="d-none d-md-block">
            <img
              src={loginImage}
              alt="Login visual"
              className="img-fluid h-100 w-100"
              style={{ objectFit: "cover", borderRadius: "0.5rem 0 0 0.5rem" }}
            />
          </MDBCol>

          <MDBCol md="6">
            <MDBCardBody className="d-flex flex-column justify-content-center">
              <h4 className="mb-4 text-center fw-bold">Welcome Back</h4>
              <p className="text-muted text-center mb-4">
                Sign in to continue to Fordis Ludus
              </p>

              {errorMsg && (
                <div className="alert alert-danger text-center" role="alert">
                  {errorMsg}
                </div>
              )}

              <MDBValidation onSubmit={handleLogin} noValidate>
                <MDBValidationItem feedback="Email is required" invalid>
                  <MDBInput
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    label="Email"
                    id="login-email"
                    name="email"
                    required
                    className="mb-3"
                    aria-label="Email address"
                  />
                </MDBValidationItem>

                <MDBValidationItem feedback="Password is required" invalid>
                  <MDBInput
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    label="Password"
                    id="login-password"
                    name="password"
                    required
                    className="mb-3"
                    aria-label="Password"
                  />
                </MDBValidationItem>

                <div className="d-flex justify-content-between mb-4">
                  <Link
                    to="/reset-password"
                    className="small text-primary"
                    aria-label="Reset your password"
                  >
                    Reset password?
                  </Link>
                  <Link
                    to="/register"
                    className="small text-primary"
                    aria-label="Create a new account"
                  >
                    Register
                  </Link>
                </div>

                <MDBBtn type="submit" className="w-100 fw-bold mb-4">
                  Login
                </MDBBtn>
              </MDBValidation>
            </MDBCardBody>
          </MDBCol>
        </MDBRow>
      </MDBCard>
    </MDBContainer>
  );
}
