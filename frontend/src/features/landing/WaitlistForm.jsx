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

  const handleSubmit = (e) => {
    e.preventDefault();

    // 🚫 Bot trap: if any honeypot field is filled, reject
    if (homepage || phone || linkedin) {
      console.warn('🤖 Bot submission blocked (honeypot triggered)');
      return;
    }

    // ✅ Real user submission
    console.log({
      email,
      name,
      role,
      feedback,
    });

    // TODO: send this to your backend API
  };

  // Accessible, invisible styles
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
      >
        <option value="">Select Role</option>
        <option value="Trader">Trader</option>
        <option value="Manager">Manager</option>
        <option value="Enterprise">Enterprise</option>
        <option value="Other">Other</option>
      </select>
      <MDBInput
        label="What would you like to see in Fordis Ludus?"
        type="textarea"
        rows={3}
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        className="mb-3"
        aria-label="Feedback"
      />

      {/* 🕵️‍♀️ Honeypot fields — visible to bots only */}
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
        Join the Waitlist
      </MDBBtn>
    </form>
  );
}
