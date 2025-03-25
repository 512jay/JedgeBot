import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

export function renderWithProviders(ui, { route = "/", authContextValue = null } = {}) {
  const Wrapper = ({ children }) => {
    return (
      <AuthProviderOverride value={authContextValue}>
        <MemoryRouter initialEntries={[route]}>
          {children}
        </MemoryRouter>
      </AuthProviderOverride>
    );
  };

  return render(ui, { wrapper: Wrapper });
}

// Wrapper that overrides the AuthContext with test values
import { AuthContext } from "../context/AuthContext";
export const AuthProviderOverride = ({ children, value }) => (
  <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
);
