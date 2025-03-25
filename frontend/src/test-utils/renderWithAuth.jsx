// /frontend/src/test-utils/renderWithAuth.jsx
import React from "react";
import { render } from "@testing-library/react";
import { AuthProvider } from "../context/AuthContext";
import { BrowserRouter } from "react-router-dom";

const renderWithAuth = (ui) => {
  return render(
    <BrowserRouter>
      <AuthProvider>{ui}</AuthProvider>
    </BrowserRouter>
  );
};

export default renderWithAuth;
