/// <reference types="vitest" />
import { describe, it, vi, expect, beforeEach } from "vitest";
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { renderWithProviders } from "../test-utils/renderWithProviders";
import Sidebar from "../components/layout/Sidebar";
import { MemoryRouter, Routes, Route, useLocation } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import * as authApi from "../api/auth_api";

// ✅ Mock only the API function
vi.mock("../api/auth_api", async () => {
  const mod = await vi.importActual("../api/auth_api");
  return {
    ...mod,
    logout: vi.fn(() => Promise.resolve({ status: 200 })),
  };
});

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
        <MemoryRouter initialEntries={["/dashboard"]}>
          <Routes>
            <Route path="*" element={<Sidebar />} />
            <Route path="*" element={<LocationDisplay />} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    );

    const button = screen.getByRole("button", { name: /logout/i });
    fireEvent.click(button);

    await waitFor(() => {
      expect(authApi.logout).toHaveBeenCalled();
    });

    await waitFor(() => {
      const location = screen.getByTestId("location-display");
      expect(location.textContent).toBe("/login");
    });
  });
});
