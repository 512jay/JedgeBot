/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import DashboardCards from "../components/DashboardCards";

describe("DashboardCards Component", () => {
  test("renders Portfolio Overview card", () => {
    render(<DashboardCards />);
    expect(screen.getByText(/portfolio overview/i)).toBeInTheDocument();
    expect(screen.getByText(/total balance/i)).toBeInTheDocument();
    expect(screen.getByText(/\$125,000/i)).toBeInTheDocument();
    expect(screen.getByText(/\+5.2%/i)).toBeInTheDocument();
  });

  test("renders Recent Activity card", () => {
    render(<DashboardCards />);
    expect(screen.getByText(/recent activity/i)).toBeInTheDocument();
    expect(screen.getByText(/executed order/i)).toBeInTheDocument();
    expect(screen.getByText(/new client added/i)).toBeInTheDocument();
    expect(screen.getByText(/portfolio rebalanced/i)).toBeInTheDocument();
  });

  test("renders Market Insights card", () => {
    render(<DashboardCards />);
    expect(screen.getByText(/market insights/i)).toBeInTheDocument();
    expect(screen.getByText(/s&p 500/i)).toBeInTheDocument();
    expect(screen.getByText(/\+1.8%/i)).toBeInTheDocument();
    expect(screen.getByText(/tsla/i)).toBeInTheDocument();
    expect(screen.getByText(/\+7.4%/i)).toBeInTheDocument();
  });
});
