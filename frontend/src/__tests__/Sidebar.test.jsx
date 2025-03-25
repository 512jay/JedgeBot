/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { renderWithProviders } from "../test-utils/renderWithProviders";
import Sidebar from "../components/layout/Sidebar";
import { AuthProvider } from "../context/AuthContext";
import * as authApi from "../api/auth_api";
import { useLocation, Routes, Route } from "react-router-dom";

// ✅ Mock only logout API function
vi.mock("../api/auth_api", async () => {
  const mod = await vi.importActual("../api/auth_api");
  return {
    ...mod,
    logout: vi.fn(() => Promise.resolve({ status: 200 })),
  };
});

// ✅ Display current route
function LocationDisplay() {
  const location = useLocation();
  return <div data-testid="location-display">{location.pathname}</div>;
}

describe("Sidebar", () => {
  beforeEach(() => {
    authApi.logout.mockClear();

    // Patch fetch to resolve relative URLs and mock responses
    global.fetch = vi.fn((url, options) => {
      const base = import.meta.env.VITE_API_BASE_URL;
      const resolvedUrl = typeof url === "string" && url.startsWith("/")
        ? `${base}${url}`
        : url;

      if (resolvedUrl.includes("/auth/me")) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            email: "test@example.com",
            role: "client"
          }),
        });
      }

      if (resolvedUrl.includes("/auth/logout")) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({}),
        });
      }

      return Promise.reject(new Error("Unhandled request to: " + resolvedUrl));
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
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
