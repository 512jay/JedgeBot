// /frontend/src/features/landing/Pricing.jsx
import React from 'react';

export default function Pricing() {
  return (
    <div
      className="d-flex flex-column align-items-center justify-content-center"
      style={{ minHeight: 'calc(100vh - 120px)' }} // Adjust for header/footer
    >
      <div
        className="d-flex rounded shadow overflow-hidden mb-4"
        style={{ maxWidth: '900px', width: '100%', backgroundColor: 'white' }}
        aria-labelledby="pricing-heading"
      >
        <div className="d-none d-md-block" style={{ flex: 1 }}>
          <img
            src="/images/pricing.jpg"
            alt="Close-up of a person holding cash in a wallet"
            className="img-fluid h-100 w-100 object-fit-cover"
            style={{ objectFit: 'cover' }}
          />
        </div>
        <div
          className="p-4 d-flex flex-column justify-content-center"
          style={{ flex: 1 }}
        >
          <h2 id="pricing-heading">Pricing</h2>
          <ul>
            <li><strong>Free:</strong> 1 brokerage account – perfect for testing the waters.</li>
            <li>
              <strong>Client ($30/month):</strong> Manage up to 10 accounts and access strategy automation with ease.
            </li>
            <li>
              <strong>Manager ($200/month):</strong> Control up to 100 accounts. Designed for professionals managing multiple clients.
            </li>
            <li>
              <strong>Enterprise:</strong> Need more? Get in touch to discuss pricing, compliance, and custom features.
            </li>
          </ul>
        </div>
      </div>

      <div className="table-responsive" style={{ maxWidth: '960px', width: '100%' }}>
        <table className="table text-center shadow-sm animated-table">
          <thead className="table-light">
            <tr>
              <th>Feature</th>
              <th>Free</th>
              <th>Client ($30/mo)</th>
              <th>Manager ($200/mo)</th>
              <th>Enterprise</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td># of Brokerage Accounts</td>
              <td>1</td>
              <td>Up to 10</td>
              <td>Up to 100</td>
              <td>Unlimited</td>
            </tr>
            <tr>
              <td>Strategy Support</td>
              <td>Basic</td>
              <td>Standard</td>
              <td>Advanced</td>
              <td>Custom</td>
            </tr>
            <tr>
              <td>Priority Support</td>
              <td><span className="xmark">✗</span></td>
              <td><span className="checkmark">✓</span></td>
              <td><span className="checkmark">✓</span></td>
              <td>VIP</td>
            </tr>
            <tr>
              <td>Manage Clients</td>
              <td><span className="xmark">✗</span></td>
              <td><span className="xmark">✗</span></td>
              <td><span className="checkmark">✓</span></td>
              <td><span className="checkmark">✓</span></td>
            </tr>
            <tr>
              <td>Onboarding Assistance</td>
              <td><span className="xmark">✗</span></td>
              <td><span className="xmark">✗</span></td>
              <td><span className="xmark">✗</span></td>
              <td>Negotiable</td>
            </tr>
            <tr>
              <td>Custom Reporting</td>
              <td><span className="xmark">✗</span></td>
              <td><span className="xmark">✗</span></td>
              <td><span className="xmark">✗</span></td>
              <td><span className="checkmark">✓</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
