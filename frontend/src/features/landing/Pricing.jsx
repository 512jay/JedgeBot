// /frontend/src/features/landing/Pricing.jsx
import { MDBContainer } from "mdb-react-ui-kit";
import { Link } from "react-router-dom";

export default function Pricing() {
  return (
    <MDBContainer className="py-5 text-center">
      <h2 className="fw-bold mb-4">Pricing</h2>
      <p className="text-muted mb-5">Choose the plan that works best for you</p>

      <div className="table-responsive">
        <table className="table table-bordered table-striped align-middle text-start shadow-sm">
          <thead className="table-dark">
            <tr>
              <th scope="col">Plan</th>
              <th scope="col">Price</th>
              <th scope="col">Accounts</th>
              <th scope="col">Support</th>
              <th scope="col">Access</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td scope="row">Free</td>
              <td>$0</td>
              <td>1 brokerage account</td>
              <td>Email only</td>
              <td>Basic features</td>
            </tr>
            <tr>
              <td scope="row">Client</td>
              <td>$30/month</td>
              <td>Up to 10 accounts</td>
              <td>Email + Chat</td>
              <td>Full dashboard access</td>
            </tr>
            <tr>
              <td scope="row">Manager</td>
              <td>$200/month</td>
              <td>Unlimited clients + accounts</td>
              <td>Priority support</td>
              <td>Client management tools</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p className="mt-4">
        Want early access?{" "}
        <Link to="/waitlist" className="fw-bold text-decoration-underline">
          Join the waitlist
        </Link>
      </p>
    </MDBContainer>
  );
}
