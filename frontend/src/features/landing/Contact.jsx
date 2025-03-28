import React from 'react';
import { Form, Button, Card } from 'react-bootstrap';

export default function Contact() {
  return (
    <Card className="shadow-sm">
      <Card.Body className="p-5">
        <h2 className="text-center mb-4">Contact Us</h2>
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Your Email</Form.Label>
            <Form.Control type="email" required placeholder="Enter your email" />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Message</Form.Label>
            <Form.Control 
              as="textarea" 
              rows={4} 
              required 
              placeholder="Your message" 
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
  );
}