// /frontend/src/features/landing/Contact.jsx

import contactImage from "@/images/hero/contact.jpg";
import React, { useState } from "react";
import { Form, Button, Card, Container, Alert, Spinner } from "react-bootstrap";

export default function Contact() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState(null); // "success", "error"
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    setLoading(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, message }),
      });
      if (!res.ok) throw new Error("Failed to send");
      setStatus("success");
      setEmail("");
      setMessage("");
    } catch {
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container
      fluid
      className="d-flex flex-column align-items-center justify-content-center"
      style={{ minHeight: "calc(100vh - 120px)" }}
    >
      <img
        src={contactImage}
        alt="Professional reviewing data on laptop"
        className="img-fluid mb-4 rounded shadow-sm"
        style={{ maxHeight: "300px", objectFit: "cover", width: "100%", maxWidth: "900px" }}
      />

      <Card className="shadow-sm hover-grow" style={{ maxWidth: "600px", width: "100%" }}>
        <Card.Body className="p-5">
          <h2 className="text-center mb-4">Contact Us</h2>

          {status === "success" && (
            <Alert variant="success">Your message has been sent successfully!</Alert>
          )}
          {status === "error" && (
            <Alert variant="danger">There was a problem sending your message. Try again later.</Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Your Email</Form.Label>
              <Form.Control
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                required
                placeholder="Your message"
                aria-label="Your message"
              />
            </Form.Group>

            <div className="text-center">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? <Spinner size="sm" animation="border" /> : "Send Message"}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
}
