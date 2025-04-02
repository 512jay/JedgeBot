// /frontend/src/features/auth/Register.jsx
import registrationImage from "@/images/hero/register.jpg";
import { register } from './auth_api';
import { useNavigate } from 'react-router-dom';

import React, { useState } from 'react';
import {
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn,
  MDBRow,
  MDBCol,
  MDBDropdown,
  MDBDropdownToggle,
  MDBDropdownMenu,
  MDBDropdownItem,
} from 'mdb-react-ui-kit';

export default function Register() {
  const [role, setRole] = useState('Choose a role');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    setError('');
    if (password !== confirmPassword) {
      return setError('Passwords do not match');
    }

    if (role === 'Choose a role') {
      return setError('Please select a role');
    }

    try {
      setLoading(true);
      const response = await register({
        email,
        password,
        role: role.toLowerCase(),
        username: email.split('@')[0], // or collect username separately
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || 'Registration failed');
      }

      navigate('/login');
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <MDBContainer fluid className="d-flex justify-content-center align-items-center" style={{ minHeight: 'calc(100vh - 120px)' }}>
      <MDBCard className="hover-grow d-flex flex-row overflow-hidden shadow" style={{ maxWidth: '850px', width: '100%' }}>
        <MDBCol md="6" className="d-none d-md-block">
          <img
            src={registrationImage}
            alt="Three women talking at a registration table"
            className="img-fluid h-100 w-100 object-fit-cover"
            style={{ objectFit: 'cover' }}
          />
        </MDBCol>
        <MDBCardBody className="p-5 d-flex flex-column justify-content-center" style={{ flex: 1 }}>
          <h4 className="mb-4 text-center">Create your account</h4>

          <label htmlFor="registerEmail" className="sr-only">Email address</label>
          <MDBInput id="registerEmail" label="Email address" type="email" className="mb-4" required value={email} onChange={(e) => setEmail(e.target.value)} />
          <label htmlFor="registerPassword" className="sr-only">Password</label>
          <MDBInput id="registerPassword" label="Password" type="password" className="mb-4" required value={password} onChange={(e) => setPassword(e.target.value)} />
          <label htmlFor="registerConfirm" className="sr-only">Confirm Password</label>
          <MDBInput id="registerConfirm" label="Confirm Password" type="password" className="mb-4" required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
          <label htmlFor="roleDropdown" className="sr-only">Select Role</label>
          <MDBDropdown className="mb-4">
            <MDBDropdownToggle color="light" id="roleDropdown">{role}</MDBDropdownToggle>
            <MDBDropdownMenu>
              {['Free', 'Client', 'Manager', 'Enterprise'].map((option) => (
                <MDBDropdownItem key={option} onClick={() => setRole(option)}>
                  {option}
                </MDBDropdownItem>
              ))}
            </MDBDropdownMenu>
          </MDBDropdown>

          <MDBBtn className="btn-primary w-100 mb-3" onClick={handleSubmit} disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </MDBBtn>
          {error && <div className="text-danger text-center mb-3">{error}</div>}
          <div className="text-center">
            <small>Already have an account? <a href="/login">Login</a></small>
          </div>
        </MDBCardBody>
      </MDBCard>
    </MDBContainer>
  );
}
