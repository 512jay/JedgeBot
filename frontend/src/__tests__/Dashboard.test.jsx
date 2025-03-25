// /frontend/src/__tests__/Dashboard.test.jsx
import { screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import Dashboard from "../pages/Dashboard";
import { renderWithProviders } from "../test-utils/renderWithProviders";

const mockUser = {
  username: "testuser",
  role: "client",
};

describe("Dashboard Page", () => {
  it("renders welcome heading", () => {
    renderWithProviders(<Dashboard />, {
      authContextValue: { user: mockUser, loading: false },
    });
    expect(
      screen.getByText(/welcome to your dashboard/i)
    ).toBeInTheDocument();
  });

  it("renders portfolio, activity, and market insights cards", () => {
    renderWithProviders(<Dashboard />, {
      authContextValue: { user: mockUser, loading: false },
    });

    expect(screen.getByText(/portfolio overview/i)).toBeInTheDocument();
    expect(screen.getByText(/recent activity/i)).toBeInTheDocument();
    expect(screen.getByText(/market insights/i)).toBeInTheDocument();
  });

  it("renders the sidebar with navigation links", () => {
    renderWithProviders(<Dashboard />, {
      authContextValue: { user: mockUser, loading: false },
    });

    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/profile/i)).toBeInTheDocument();
  });

  it("redirects unauthorized roles", () => {
    const mockNavigator = vi.fn();

    renderWithProviders(<Dashboard />, {
      authContextValue: {
        user: { username: "hacker", role: "evil" },
        loading: false,
      },
      routerProps: {
        navigator: { push: mockNavigator },
        location: { pathname: "/" },
      },
    });

    expect(mockNavigator).toHaveBeenCalledWith("/unauthorized");
  });
});
