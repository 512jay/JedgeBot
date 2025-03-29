// /frontend/src/components/layouts/LoadingScreen.jsx
import React from "react";
import { MDBSpinner } from "mdb-react-ui-kit";

const LoadingScreen = () => (
  <div className="d-flex justify-content-center align-items-center vh-100">
    <MDBSpinner role="status" />
  </div>
);

export default LoadingScreen;
