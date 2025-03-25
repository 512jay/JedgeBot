// /frontend/src/__tests__/Dashboard.test.jsx
import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import { AuthContext } from "../../../context/AuthContext";

const mockUser = { role: "client" };

const renderDashboard = (user = mockUser, loading = false) => {
  return render(
    <AuthContext.Provider value={{ user, loading }}>
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>
    </AuthContext.Provider>
  );
};

describe("Dashboard Page", () => {
  it("renders welcome heading", () => {
    renderDashboard();
    expect(screen.getByText(/welcome to your dashboard/i)).toBeInTheDocument();
  });

  it("renders portfolio overview card", () => {
    renderDashboard();
    expect(screen.getByText(/portfolio overview/i)).toBeInTheDocument();
    expect(screen.getByText(/total balance/i)).toBeInTheDocument();
    expect(screen.getByText(/net p&l/i)).toBeInTheDocument();
  });

  it("renders recent activity section", () => {
    renderDashboard();
    expect(screen.getByText(/recent activity/i)).toBeInTheDocument();
    expect(screen.getByText(/executed order/i)).toBeInTheDocument();
    expect(screen.getByText(/new client added/i)).toBeInTheDocument();
    expect(screen.getByText(/portfolio rebalanced/i)).toBeInTheDocument();
  });

  it("renders market insights section", () => {
    renderDashboard();
    expect(screen.getByText(/market insights/i)).toBeInTheDocument();
    expect(screen.getByText(/s&p 500/i)).toBeInTheDocument();
    expect(screen.getByText(/top gainer/i)).toBeInTheDocument();
  });
});