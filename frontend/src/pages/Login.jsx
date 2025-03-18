import React from 'react';
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn
} from 'mdb-react-ui-kit';

function Login() {
  return (
    <section className="vh-100" style={{ backgroundColor: '#9A616D' }}>
      <MDBContainer className="py-5 h-100">
        <MDBRow className="d-flex justify-content-center align-items-center h-100">
          <MDBCol md="10">
            <MDBCard className="border-0" style={{ borderRadius: '1rem' }}>
              <MDBRow className="g-0">
                
                {/* Left Side Image */}
                <MDBCol md="6" lg="5" className="d-none d-md-block">
                  <img
                    src="/leftlogin.jpg"
                    alt="A Black woman in a business suit working on a laptop, symbolizing disability inclusion and accessibility in professional spaces."
                    className="img-fluid"
                    style={{ borderRadius: '1rem 0 0 1rem' }}
                  />
                </MDBCol>

                {/* Right Side Login Form */}
                <MDBCol md="6" lg="7" className="d-flex align-items-center">
                  <MDBCardBody className="p-4 p-lg-5 text-black">
                    <form onSubmit={(e) => e.preventDefault()}>
                      
                      {/* Logo Section */}
                      <div className="d-flex align-items-center mb-3 pb-1">
                        <i className="fas fa-cubes fa-2x me-3" style={{ color: '#ff6219' }}></i>
                        <span className="h1 fw-bold mb-0">Logo</span>
                      </div>

                      {/* Heading */}
                      <h5 className="fw-normal mb-3 pb-3" style={{ letterSpacing: '1px' }}>
                        Sign into your account
                      </h5>

                      {/* Email Input */}
                      <MDBInput
                        wrapperClass="mb-4"
                        label="Email address"
                        id="login-email"
                        type="email"
                        size="lg"
                        required
                        autoComplete="username"
                      />

                      {/* Password Input */}
                      <MDBInput
                        wrapperClass="mb-4"
                        label="Password"
                        id="login-password"
                        type="password"
                        size="lg"
                        required
                        autoComplete="current-password"
                      />

                      {/* Login Button */}
                      <div className="pt-1 mb-4">
                        <MDBBtn color="dark" size="lg" className="w-100" type="submit">
                          Login
                        </MDBBtn>
                      </div>

                      {/* Links */}
                      <a className="small text-muted" href="#!">
                        Forgot password?
                      </a>
                      <p className="mb-5 pb-lg-2" style={{ color: '#393f81' }}>
                        Don't have an account? <a href="register" style={{ color: '#393f81' }}>Register here</a>
                      </p>
                      <a href="#!" className="small text-muted">Terms of use.</a>
                      <a href="#!" className="small text-muted">Privacy policy</a>
                    </form>
                  </MDBCardBody>
                </MDBCol>

              </MDBRow>
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </section>
  );
}

export default Login;
