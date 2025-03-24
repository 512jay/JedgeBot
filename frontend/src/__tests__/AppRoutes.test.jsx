/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AppRoutes } from "../AppRoutes";
import { renderWithProviders } from "@/../test-utils/renderWithProviders";


// Mock pages
vi.mock("../pages/Login", () => ({ default: () => <div>Login Page</div> }));
vi.mock("../pages/Register", () => ({ default: () => <div>Register Page</div> }));
vi.mock("../pages/Landing", () => ({ default: () => <div>Landing Page</div> }));
vi.mock("../pages/ForgotPassword", () => ({ default: () => <div>Forgot Password</div> }));
vi.mock("../pages/ResetPassword", () => ({ default: () => <div>Reset Password</div> }));
vi.mock("../layouts/DashboardLayout", () => ({
  default: () => (
    <div>
      Dashboard Layout
      <Outlet />
    </div>
  ),
}));
vi.mock("../components/DashboardCards", () => ({
  default: () => <div>Dashboard Cards</div>,
}));

describe("AppRoutes", () => {
  it("renders dashboard index (DashboardCards)", () => {
    renderWithProviders(<AppRoutes useBrowserRouter={false} />, {
      route: "/dashboard",
      authContextValue: {
        user: { email: "test@example.com", role: "client" },
        login: vi.fn(),
        logout: vi.fn(),
      },
    });

    expect(screen.getByText(/welcome to your dashboard/i)).toBeInTheDocument();
  });
});
