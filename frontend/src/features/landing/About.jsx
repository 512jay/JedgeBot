// /frontend/src/features/landing/About.jsx
import aboutImage from "@/images/about.jpg";
import React from 'react';

export default function About() {
  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ minHeight: 'calc(100vh - 120px)' }}
    >
      <div
        className="d-flex flex-column flex-md-row rounded shadow overflow-hidden hover-grow"
        style={{ maxWidth: '800px', width: '100%', backgroundColor: 'white' }}
        aria-labelledby="about-heading"
        role="region"
        aria-label="About Section"
      >
        {/* 🖼️ Image */}
        <div style={{ flex: 1 }}>
          <img
            src={aboutImage}
            alt="Illuminated sign saying 'Think About Things Differently'"
            className="img-fluid w-100"
            style={{
              height: '100%',
              maxHeight: '400px',
              objectFit: 'cover',
              objectPosition: 'center',
            }}
          />
        </div>

        {/* 📄 Text content */}
        <div
          className="p-4 d-flex flex-column justify-content-center text-center text-md-start"
          style={{ flex: 1 }}
        >
          <h2 id="about-heading">About Fordis Ludus</h2>
          <p>
            Fordis Ludus is built by a trader and developer committed to making
            multi-account management simple, powerful, and accessible.
          </p>
          <p>
            The name <strong>Fordis Ludus</strong> is Latin for <em>Brave Game</em> — a tribute
            to bold thinkers who approach investing with confidence, creativity,
            and strategy. We believe you deserve tools that match your courage
            and ambition.
          </p>
        </div>
      </div>
    </div>
  );
}
