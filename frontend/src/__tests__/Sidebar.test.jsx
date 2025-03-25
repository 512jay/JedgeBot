// /frontend/src/__tests__/Sidebar.test.jsx
import { describe, it, vi, expect } from "vitest";
import { screen, fireEvent, waitFor } from "@testing-library/react";
import { renderWithProviders } from "../test-utils/renderWithProviders";
import Sidebar from "../components/layout/Sidebar";

// Mock the logout function
const mockLogout = vi.fn(() => Promise.resolve());

describe("Sidebar", () => {
  it("calls logout and navigates on Logout button click", async () => {
    renderWithProviders(<Sidebar />, {
      authContextValue: { logout: mockLogout },
    });

    const button = screen.getByRole("button", { name: /logout/i });
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockLogout).toHaveBeenCalled();
    });
  });
});
