// /frontend/src/features/landing/Landing.jsx
import heroImage from "@/images/hero/landing.jpg";
import WaitlistForm from "@/features/landing/WaitlistForm";

export default function Landing() {
  return (
    <>
      {/* 🔹 Desktop layout */}
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
            <WaitlistCard />
          </div>
        </div>
      </div>

      {/* 🔹 Mobile layout */}
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
          <WaitlistCard />
        </section>
      </div>
    </>
  );
}

function WaitlistCard() {
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

      <WaitlistForm />
    </div>
  );
}
