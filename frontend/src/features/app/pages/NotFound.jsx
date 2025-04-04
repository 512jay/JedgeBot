// /frontend/src/features/app/pages/NotFound.jsx
import { Link } from "react-router-dom";
import NotFoundImage from "@images/hero/pageNotFound.webp"; // or .webp etc

export default function NotFound() {
  return (
    <div className="text-center p-5">
      <img
        src={NotFoundImage}
        alt="404 - Page not found"
        style={{ maxWidth: "400px" }}
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
