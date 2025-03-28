import React from 'react';
import { MDBInput, MDBBtn } from 'mdb-react-ui-kit';

export default function Contact() {
  return (
    <div className="p-5">
      <h2>Contact Us</h2>
      <form>
        <MDBInput label='Your Email' type='email' required className='mb-3' />
        <MDBInput label='Message' type='textarea' rows={4} required className='mb-3' />
        <MDBBtn>Send Message</MDBBtn>
      </form>
    </div>
  );
}

