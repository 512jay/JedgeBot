import React, { useState } from 'react';
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn,
  MDBRadio,
} from 'mdb-react-ui-kit';

function Register() {
  const [plan, setPlan] = useState('free');

  const handlePlanChange = (value) => {
    setPlan(value);
  };

  return (
    <section className="vh-100" style={{ backgroundColor: '#9A616D' }}>
      <MDBContainer className="py-5 h-100">
        <MDBRow className="d-flex justify-content-center align-items-center h-100">
          <MDBCol md="8">
            <MDBCard className="border-0" style={{ borderRadius: '1rem' }}>
              <MDBCardBody className="p-4 text-black">
                <h2 className="text-center fw-bold mb-4">Create an Account</h2>

                <form onSubmit={(e) => e.preventDefault()}>
                  {/* Email */}
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Email address"
                    id="register-email"
                    type="email"
                    size="lg"
                    required
                    autoComplete="email"
                  />

                  {/* Password */}
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Password"
                    id="register-password"
                    type="password"
                    size="lg"
                    required
                    autoComplete="new-password"
                  />

                  {/* Confirm Password */}
                  <MDBInput
                    wrapperClass="mb-4"
                    label="Confirm Password"
                    id="register-confirm-password"
                    type="password"
                    size="lg"
                    required
                  />

                  {/* Subscription Plan */}
                  <h5 className="fw-bold mb-3">Choose Your Plan</h5>
                  <MDBRadio name="plan" label="Free (1 brokerage account)" value="free"
                    checked={plan === 'free'} onChange={() => handlePlanChange('free')} />
                  <MDBRadio name="plan" label="Paid Client ($30/month - 10 accounts)" value="paid"
                    checked={plan === 'paid'} onChange={() => handlePlanChange('paid')} />
                  <MDBRadio name="plan" label="Manager ($200/month - Unlimited clients & accounts)" value="manager"
                    checked={plan === 'manager'} onChange={() => handlePlanChange('manager')} />

                  {/* Register Button */}
                  <MDBBtn color="dark" size="lg" className="w-100" type="submit">
                    Register
                  </MDBBtn>

                  <p className="text-center mt-3">
                    Already have an account? <a href="/login" style={{ color: '#393f81' }}>Log in</a>
                  </p>
                </form>
              </MDBCardBody>
            </MDBCard>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </section>
  );
}

export default Register;
