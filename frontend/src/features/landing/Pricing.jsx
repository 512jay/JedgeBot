// /frontend/src/features/landing/Pricing.jsx
import React from 'react';

export default function Pricing() {
  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ minHeight: 'calc(100vh - 120px)' }} // header + footer
    >
      <div
        className="d-flex rounded shadow overflow-hidden"
        style={{ maxWidth: '900px', width: '100%', backgroundColor: 'white' }}
        aria-labelledby="pricing-heading"
      >
        <div className="d-none d-md-block" style={{ flex: 1 }}>
          <img
            src="/images/pricing.jpg"
            alt="A person pulling cash from a wallet, symbolizing investment decisions"
            className="img-fluid h-100 w-100 object-fit-cover"
            style={{ objectFit: 'cover' }}
          />
        </div>
        <div
          className="p-4 d-flex flex-column justify-content-center"
          style={{ flex: 1 }}
        >
          <h2 id="pricing-heading">Plans That Grow With You</h2>
          <p>
            Whether you're just getting started or managing dozens of accounts, Fordis Ludus
            meets you where you are—and helps you go further.
          </p>

          <ul className="list-unstyled">
            <li className="mb-3">
              <strong>🌱 Free:</strong>{' '}
              Perfect for individual traders testing the waters. Connect 1 brokerage account and experience the core platform—no strings attached.
            </li>
            <li className="mb-3">
              <strong>🚀 Client ($30/month):</strong>{' '}
              Serious about scaling? Manage up to 10 accounts with streamlined automation and professional tools to grow your portfolio.
            </li>
            <li className="mb-3">
              <strong>🏢 Manager ($200/month):</strong>{' '}
              Designed for growing firms and advanced advisors. Manage up to <strong>100 accounts</strong>, with access to detailed analytics, compliance exports, and white-glove support.
            </li>
            <li className="mb-3">
              <strong>🏛️ Enterprise:</strong>{' '}
              Built for institutions. Manage unlimited managers and accounts across teams. <a href="/contact">Contact us for pricing</a> and tailored onboarding.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
