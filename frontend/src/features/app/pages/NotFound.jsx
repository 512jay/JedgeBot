// /frontend/src/app/pages/NotFound.jsx
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="text-center p-5">
      <img
        src="/images/404.png"
        alt="404 - Page not found"
        style={{ maxWidth: "300px" }}
        className="img-fluid mb-4"
      />
      <h1 className="text-danger fw-bold">404</h1>
      <h2 className="mb-3">Page not found</h2>
      <p className="mb-4">
        Sorry, the page you were looking for doesn't exist or has been moved.
      </p>
      <Link to="/" className="btn btn-primary">
        Go to Homepage
      </Link>
    </div>
  );
}
