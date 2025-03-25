// /frontend/src/test-utils/renderWithProviders.jsx
// Utility for wrapping test components with app context providers

import React from "react";
import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AuthContext } from "../context/AuthContext"; // ✅ Adjust path if needed

// Add any other providers here (theme, data, etc.)
export function renderWithProviders(
  ui,
  {
    route = "/",
    authContextValue = {},
  } = {}
) {
  const Wrapper = ({ children }) => {
    return (
      <AuthContext.Provider value={authContextValue}>
        <MemoryRouter initialEntries={[route]}>
          {children}
        </MemoryRouter>
      </AuthContext.Provider>
    );
  };

  return render(ui, { wrapper: Wrapper });
}
