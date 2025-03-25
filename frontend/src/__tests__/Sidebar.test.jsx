/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { renderWithProviders } from "../test-utils/renderWithProviders";
import Sidebar from "../components/layout/Sidebar";
import { AuthProvider } from "../context/AuthContext";
import * as authApi from "../api/auth_api";
import { useLocation, Routes, Route } from "react-router-dom";

// ✅ Mock the logout API call only
vi.mock("../api/auth_api", async () => {
  const mod = await vi.importActual("../api/auth_api");
  return {
    ...mod,
    logout: vi.fn(() => Promise.resolve({ status: 200 })),
  };
});

// ✅ Utility component to detect route changes
function LocationDisplay() {
  const location = useLocation();
  return <div data-testid="location-display">{location.pathname}</div>;
}

describe("Sidebar", () => {
  beforeEach(() => {
    authApi.logout.mockClear();
  });

  it("logs out and navigates to /login", async () => {
    renderWithProviders(
      <AuthProvider>
        <Routes>
          <Route path="*" element={<><Sidebar /><LocationDisplay /></>} />
        </Routes>
      </AuthProvider>,
      {
        route: "/dashboard",
      }
    );

    const logoutBtn = screen.getByRole("button", { name: /logout/i });
    fireEvent.click(logoutBtn);

    await waitFor(() => {
      expect(authApi.logout).toHaveBeenCalled();
    });

    await waitFor(() => {
      expect(screen.getByTestId("location-display").textContent).toBe("/login");
    });
  });
});
