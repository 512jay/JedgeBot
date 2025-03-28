// /frontend/src/features/auth/pages/Register.jsx
import { Link } from "react-router-dom";
import {
  MDBBtn,
  MDBCardBody,
  MDBCol,
  MDBInput,
  MDBRow,
} from "mdb-react-ui-kit";
import registerImage from "@images/registration.jpg"; // updated path

export default function Register() {
  return (
    <div
      className="card-hover shadow-lg rounded-5 overflow-hidden bg-white mx-auto"
      style={{ maxWidth: "960px", width: "100%" }}
      role="region"
      aria-labelledby="register-heading"
    >
      <MDBRow className="g-0">
        <MDBCol md="6">
          <img
            src={registerImage}
            alt="A welcoming registration scene with people at a desk"
            className="w-100 h-100 object-fit-cover"
          />
        </MDBCol>

        <MDBCol md="6">
          <MDBCardBody className="d-flex flex-column justify-content-center p-5">
            <h3 className="text-center mb-4" id="register-heading">
              Create your account
            </h3>

            <MDBInput
              label="Email address"
              id="register-email"
              type="email"
              className="mb-3"
              aria-label="Email address"
            />

            <MDBInput
              label="Password"
              id="register-password"
              type="password"
              className="mb-3"
              aria-label="Password"
            />

            <MDBInput
              label="Confirm Password"
              id="register-confirm-password"
              type="password"
              className="mb-4"
              aria-label="Confirm password"
            />

            <MDBBtn className="w-100 mb-3" color="primary">
              Register
            </MDBBtn>

            <div className="text-center" aria-label="Login redirect">
              Already have an account?{" "}
              <Link to="/login" className="text-decoration-underline">
                Login
              </Link>
            </div>
          </MDBCardBody>
        </MDBCol>
      </MDBRow>
    </div>
  );
}
