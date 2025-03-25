// /frontend/src/__tests__/Dashboard.test.jsx

import { screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Dashboard from "../pages/Dashboard";
import { renderWithProviders } from "../test-utils/renderWithProviders";

describe("Dashboard Page", () => {
  it("renders heading and Tailwind test div", () => {
    renderWithProviders(<Dashboard />);

    expect(screen.getByTestId("dashboard-heading")).toBeInTheDocument();
  });

  it("renders sidebar with dashboard link", () => {
    renderWithProviders(<Dashboard />);

    // Narrow the search to the sidebar
    const sidebar = screen.getByRole("navigation", { name: /main sidebar/i });
    const navLinks = within(sidebar).getAllByText(/dashboard/i);

    expect(navLinks.length).toBeGreaterThan(0);
  });
});
