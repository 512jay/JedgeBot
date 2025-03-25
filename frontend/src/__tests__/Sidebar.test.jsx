/// <reference types="vitest" />
import { describe, it, vi, expect } from "vitest";
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { renderWithProviders } from "../test-utils/renderWithProviders";
import Sidebar from "../components/layout/Sidebar";
import { MemoryRouter, useLocation } from "react-router-dom";

const mockLogout = vi.fn();

function LocationDisplay() {
  const location = useLocation();
  return <div data-testid="location-display">{location.pathname}</div>;
}

describe("Sidebar", () => {
  it("calls logout and navigates to /login on click", async () => {
    renderWithProviders(
      <>
        <Sidebar />
        <LocationDisplay />
      </>,
      {
        authContextValue: { logout: mockLogout },
        route: "/dashboard",
      }
    );

    const logoutButton = screen.getByRole("button", { name: /logout/i });
    fireEvent.click(logoutButton);

    await waitFor(() => {
      expect(mockLogout).toHaveBeenCalled();
    });

    // Simulate navigation effect
    await waitFor(() => {
      const location = screen.getByTestId("location-display");
      expect(location.textContent).toBe("/login");
    });
  });
});
