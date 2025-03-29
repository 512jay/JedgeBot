// /frontend/src/features/landing/Contact.jsx
import contactImage from "@/images/contact.jpg";
import React from 'react';
import { Form, Button, Card, Container } from 'react-bootstrap';

export default function Contact() {
  return (
    <Container
      fluid
      className="d-flex flex-column align-items-center justify-content-center"
      style={{ minHeight: 'calc(100vh - 120px)' }} // header & footer space
    >
      <img
        src={contactImage}
        alt="Professional reviewing data on laptop"
        className="img-fluid mb-4 rounded shadow-sm"
        style={{ maxHeight: '300px', objectFit: 'cover', width: '100%', maxWidth: '900px' }}
      />

      <Card className="shadow-sm hover-grow" style={{ maxWidth: '600px', width: '100%' }}>
        <Card.Body className="p-5">
          <h2 className="text-center mb-4">Contact Us</h2>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Your Email</Form.Label>
              <Form.Control
                type="email"
                required
                placeholder="Enter your email"
                aria-label="Your email address"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Message</Form.Label>
              <Form.Control
                as="textarea"
                rows={4}
                required
                placeholder="Your message"
                aria-label="Your message"
              />
            </Form.Group>

            <div className="text-center">
              <Button variant="primary" type="submit">
                Send Message
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
}
