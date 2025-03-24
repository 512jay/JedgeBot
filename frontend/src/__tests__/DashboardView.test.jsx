// /frontend/src/__tests__/DashboardView.test.jsx

import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { renderWithProviders } from "../test-utils/renderWithProviders";
import DashboardView from "../views/DashboardView";

describe("DashboardView", () => {
  it("shows loading state", () => {
    renderWithProviders(<DashboardView />, {
      providerProps: {
        auth: { loading: true, user: null },
      },
    });

    expect(screen.getByText(/loading dashboard/i)).toBeInTheDocument();
  });

  it("redirects to login if user is not authenticated", () => {
    renderWithProviders(<DashboardView />, {
      providerProps: {
        auth: { loading: false, user: null },
      },
    });

    expect(screen.queryByText(/dashboard/i)).not.toBeInTheDocument();
  });

  it("renders client dashboard message", () => {
    renderWithProviders(<DashboardView />, {
      providerProps: {
        auth: {
          loading: false,
          user: { username: "client1", role: "client" },
        },
      },
    });

    expect(screen.getByText(/client-specific dashboard/i)).toBeInTheDocument();
  });

  it("renders manager dashboard message", () => {
    renderWithProviders(<DashboardView />, {
      providerProps: {
        auth: {
          loading: false,
          user: { username: "manager1", role: "manager" },
        },
      },
    });

    expect(screen.getByText(/manager view under construction/i)).toBeInTheDocument();
  });

  it("renders enterprise dashboard placeholder", () => {
    renderWithProviders(<DashboardView />, {
      providerProps: {
        auth: {
          loading: false,
          user: { username: "enterprise1", role: "enterprise" },
        },
      },
    });

    expect(screen.getByText(/enterprise dashboard placeholder/i)).toBeInTheDocument();
  });

  it("renders dashboard cards for free role", () => {
    renderWithProviders(<DashboardView />, {
      providerProps: {
        auth: {
          loading: false,
          user: { username: "freeloader", role: "free" },
        },
      },
    });

    expect(screen.getAllByTestId("card").length).toBeGreaterThan(0);
  });

  it("redirects to login on unknown role", () => {
    renderWithProviders(<DashboardView />, {
      providerProps: {
        auth: {
          loading: false,
          user: { username: "badrole", role: "banana" },
        },
      },
    });

    expect(screen.queryByText(/dashboard/i)).not.toBeInTheDocument();
  });
});
