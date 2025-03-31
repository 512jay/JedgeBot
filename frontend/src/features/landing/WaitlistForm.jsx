// /frontend/src/features/landing/WaitlistForm.jsx
import React, { useState } from 'react';
import { MDBInput, MDBBtn } from 'mdb-react-ui-kit';

export default function WaitlistForm() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [feedback, setFeedback] = useState('');

  // Honeypot fields
  const [homepage, setHomepage] = useState('');
  const [phone, setPhone] = useState('');
  const [linkedin, setLinkedin] = useState('');

  // Error states
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email address.';
    }

    if (!role) {
      newErrors.role = 'Please select a role.';
    }

    if (feedback.trim().length < 10) {
      newErrors.feedback = 'Please provide at least 10 characters of feedback.';
    }

    return newErrors;
  };

const handleSubmit = async (e) => {
  e.preventDefault();

  // Honeypot bot check
  if (homepage || phone || linkedin) {
    console.warn('🤖 Bot submission blocked (honeypot triggered)');
    return;
  }

  const formErrors = validate();
  if (Object.keys(formErrors).length > 0) {
    setErrors(formErrors);
    return;
  }

  setErrors({});

  try {
    const response = await fetch('/api/waitlist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        role,
        feedback,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('❌ Submission failed:', errorData);
      setErrors({ form: 'Submission failed. Please try again later.' });
      return;
    }

    const data = await response.json();
    console.log('✅ Waitlist submission successful:', data);

    // Optionally reset the form
    setName('');
    setEmail('');
    setRole('');
    setFeedback('');
  } catch (error) {
    console.error('❌ Network error during submission:', error);
    setErrors({ form: 'Network error. Please try again.' });
  }
};


  const visuallyHiddenInputStyle = {
    position: 'absolute',
    left: '-9999px',
    opacity: 0,
    height: '1px',
    width: '1px',
    pointerEvents: 'none',
  };

  return (
    <form onSubmit={handleSubmit} className="waitlist-form">
      <MDBInput
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
        className="mb-3"
        aria-label="Email"
      />
      {errors.email && <div className="text-danger small mb-2">{errors.email}</div>}

      <MDBInput
        label="Name (optional)"
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="mb-3"
        aria-label="Name"
      />

      <select
        value={role}
        onChange={(e) => setRole(e.target.value)}
        className="form-select mb-3"
        aria-label="Role"
        required
      >
        <option value="">Select Role</option>
        <option value="trader">Trader</option>
        <option value="manager">Manager</option>
        <option value="enterprise">Enterprise</option>
        <option value="client">Client</option>
      </select>
      {errors.role && <div className="text-danger small mb-2">{errors.role}</div>}

      <MDBInput
        label="What would you like to see in Fordis Ludus?"
        type="textarea"
        rows={3}
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        className="mb-3"
        aria-label="Feedback"
      />
      {errors.feedback && <div className="text-danger small mb-2">{errors.feedback}</div>}

      {/* 🕵️‍♀️ Honeypot fields — hidden from humans */}
      <div className="extra-fields" aria-hidden="true">
        <label htmlFor="homepage" className="sr-only">Company Website</label>
        <input
          type="text"
          id="homepage"
          name="homepage"
          value={homepage}
          onChange={(e) => setHomepage(e.target.value)}
          autoComplete="off"
          tabIndex="-1"
          style={visuallyHiddenInputStyle}
        />

        <label htmlFor="phone" className="sr-only">Phone Number</label>
        <input
          type="text"
          id="phone"
          name="phone"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          autoComplete="off"
          tabIndex="-1"
          style={visuallyHiddenInputStyle}
        />

        <label htmlFor="linkedin" className="sr-only">LinkedIn Profile</label>
        <input
          type="text"
          id="linkedin"
          name="linkedin"
          value={linkedin}
          onChange={(e) => setLinkedin(e.target.value)}
          autoComplete="off"
          tabIndex="-1"
          style={visuallyHiddenInputStyle}
        />
      </div>
        <MDBBtn type="submit" block>
          Request Early Access
        </MDBBtn>

        {errors.form && <div className="text-danger small mb-2">{errors.form}</div>}      
    </form>
  );
}
