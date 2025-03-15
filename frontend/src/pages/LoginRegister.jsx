import React, { useState } from 'react';
import {
  MDBContainer,
  MDBTabs,
  MDBTabsItem,
  MDBTabsLink,
  MDBTabsContent,
  MDBTabsPane,
  MDBBtn,
  MDBIcon,
  MDBInput,
  MDBCheckbox
} from 'mdb-react-ui-kit';

function LoginRegister() {
  const [justifyActive, setJustifyActive] = useState('tab1');
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [registerData, setRegisterData] = useState({ name: '', username: '', email: '', password: '' });

  const handleJustifyClick = (value) => {
    if (value !== justifyActive) setJustifyActive(value);
  };

  const handleLogin = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: loginData.username,
          password: loginData.password
        })
      });

      const result = await response.json();
      alert(`Login ${response.ok ? 'successful' : 'failed'}: ${result.access_token || result.detail}`);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const handleRegister = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: registerData.username,
          password: registerData.password
        })
      });

      const result = await response.json();
      alert(`Register ${response.ok ? 'successful' : 'failed'}: ${result.access_token || result.detail}`);
    } catch (error) {
      console.error('Register error:', error);
    }
  };

  return (
    <MDBContainer className="p-3 my-5 d-flex flex-column w-50">

      <MDBTabs pills justify className='mb-3 d-flex flex-row justify-content-between'>
        <MDBTabsItem>
          <MDBTabsLink onClick={() => handleJustifyClick('tab1')} active={justifyActive === 'tab1'}>
            Login
          </MDBTabsLink>
        </MDBTabsItem>
        <MDBTabsItem>
          <MDBTabsLink onClick={() => handleJustifyClick('tab2')} active={justifyActive === 'tab2'}>
            Register
          </MDBTabsLink>
        </MDBTabsItem>
      </MDBTabs>

      <MDBTabsContent>

        {/* Login Tab */}
        <MDBTabsPane show={justifyActive === 'tab1'}>
          <MDBInput
            wrapperClass='mb-4'
            label='Username'
            id='login-username'
            type='text'
            value={loginData.username}
            onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
          />
          <MDBInput
            wrapperClass='mb-4'
            label='Password'
            id='login-password'
            type='password'
            value={loginData.password}
            onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
          />
          <MDBBtn className="mb-4 w-100" onClick={handleLogin}>Sign in</MDBBtn>
        </MDBTabsPane>

        {/* Register Tab */}
        <MDBTabsPane show={justifyActive === 'tab2'}>
          <MDBInput
            wrapperClass='mb-4'
            label='Name'
            id='register-name'
            type='text'
            value={registerData.name}
            onChange={(e) => setRegisterData({ ...registerData, name: e.target.value })}
          />
          <MDBInput
            wrapperClass='mb-4'
            label='Username'
            id='register-username'
            type='text'
            value={registerData.username}
            onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })}
          />
          <MDBInput
            wrapperClass='mb-4'
            label='Email'
            id='register-email'
            type='email'
            value={registerData.email}
            onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })}
          />
          <MDBInput
            wrapperClass='mb-4'
            label='Password'
            id='register-password'
            type='password'
            value={registerData.password}
            onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
          />
          <MDBCheckbox wrapperClass='mb-4' label='I agree to terms' />
          <MDBBtn className="mb-4 w-100" onClick={handleRegister}>Sign up</MDBBtn>
        </MDBTabsPane>

      </MDBTabsContent>
    </MDBContainer>
  );
}

export default LoginRegister;
