// /frontend/src/features/landing/Landing.jsx
import { useState } from "react";
import {
  MDBInput,
  MDBBtn,
  MDBValidation,
  MDBValidationItem,
  MDBTextArea,
} from "mdb-react-ui-kit";
import heroImage from "@/images/hero/landing.jpg";
import { fetchWithCredentials } from "@/api/api_client";
import { toast } from "react-toastify";


export default function Landing() {
  const [formSubmitted, setFormSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const form = e.target;
    const email = form.email.value.trim();
    const name = form.name.value.trim();
    const role = form.role.value;
    const feedback = form["waitlist-feedback"].value.trim();

    const payload = {
      email,
      name: name || null,
      role,
      feedback: feedback || null,
    };

    try {
      const response = await fetchWithCredentials("/api/waitlist", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const error = await response.json();
        toast.error(error.detail || "Something went wrong.");
        return;
      }

      toast.success("You're on the waitlist! 🎉");
      setFormSubmitted(true);
    } catch (err) {
      console.error("Waitlist submission error:", err);
      toast.error("Network error. Please try again later.");
    }
  };



  return (
    <>
      {/* 🔹 Desktop version with full-width hero and border effect */}
      <div className="d-none d-md-block">
        <div
          style={{
            padding: "1.5rem",
            backgroundColor: "#9A616D",
            margin: 0,
            width: "100vw",
            position: "relative",
            left: "50%",
            right: "50%",
            marginLeft: "-50vw",
            marginRight: "-50vw",
          }}
        >
          <div
            className="position-relative overflow-hidden"
            style={{
              backgroundImage: `url(${heroImage})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
              width: "100%",
              height: "85vh",
              borderRadius: "0.75rem",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              maxWidth: "1400px",
              margin: "0 auto",
              boxShadow: "0 8px 24px rgba(0, 0, 0, 0.15)",
            }}
          >
            <WaitlistCard
              formSubmitted={formSubmitted}
              handleSubmit={handleSubmit}
            />
          </div>
        </div>
      </div>

      {/* 🔹 Mobile version (full-bleed) */}
      <div className="d-block d-md-none">
        <section
          className="d-flex align-items-center justify-content-center"
          style={{
            backgroundImage: `url(${heroImage})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            width: "100vw",
            height: "100vh",
            marginLeft: "calc(-50vw + 50%)",
          }}
        >
          <WaitlistCard
            formSubmitted={formSubmitted}
            handleSubmit={handleSubmit}
          />
        </section>
      </div>
    </>
  );
}

function WaitlistCard({ formSubmitted, handleSubmit }) {
  return (
    <div
      className="bg-white bg-opacity-75 p-4 p-md-5 rounded shadow"
      style={{ maxWidth: "500px", width: "90%", backdropFilter: "blur(5px)" }}
    >
      <h2 className="fw-bold mb-2 text-center">Get Early Access to Fordis Ludus</h2>
      <p className="text-muted text-center mb-3">
        Trade smarter. Manage more. Stress less.
      </p>
      <p className="text-center text-muted mb-4">
        Join the waitlist to try our intelligent, multi-account trading platform before anyone else.
        Be the first to shape the future of automated portfolio management.
      </p>


      {formSubmitted ? (
        <div className="alert alert-success text-center" role="alert">
          🎉 Thanks! You're on the waitlist.
        </div>
      ) : (
        <MDBValidation tag="form" onSubmit={handleSubmit} noValidate>
          <fieldset>
            <legend className="visually-hidden">Waitlist Signup</legend>

            <MDBValidationItem feedback="Email is required" invalid>
              <MDBInput
                label="Email"
                id="waitlist-email"
                name="email"
                required
                aria-label="Email address"
                className="mb-3"
              />
            </MDBValidationItem>

            <MDBInput
              label="Name (optional)"
              id="waitlist-name"
              name="name"
              aria-label="Your name"
              className="mb-3"
            />

            <div className="mb-3">
              <label htmlFor="waitlist-role" className="form-label">
                What best describes your interest?
              </label>
              <select
                id="waitlist-role"
                name="role"
                required
                className="form-select"
                aria-label="Select your intent"
              >
                <option value="">Choose...</option>
                <option value="trader">I'm just trying it out</option>
                <option value="manager">I manage other people's accounts</option>
                <option value="enterprise">I represent a larger firm or institution</option>
              </select>
            </div>



            <MDBTextArea
              label="What would you like to see from Fordis Ludus?"
              rows={3}
              id="waitlist-feedback"
              className="mb-4"
              aria-label="Suggestions or feedback"
            />

          <MDBBtn type="submit" className="w-100 fw-bold">
            Request Early Access
          </MDBBtn>

          </fieldset>
        </MDBValidation>
      )}
    </div>
  );
}