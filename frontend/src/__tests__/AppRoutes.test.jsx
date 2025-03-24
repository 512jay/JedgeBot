/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AppRoutes } from "../AppRoutes";
import { renderWithProviders } from "@/../test-utils/renderWithProviders";
import { AppRoutes } from "../AppRoutes";

renderWithProviders(<AppRoutes useBrowserRouter={false} />);


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
  test("renders landing page by default", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <AppRoutes useBrowserRouter={false} />
      </MemoryRouter>
    );
    expect(screen.getByText(/landing page/i)).toBeInTheDocument();
  });

  test("renders login page", () => {
    render(
      <MemoryRouter initialEntries={["/login"]}>
        <AppRoutes useBrowserRouter={false} />
      </MemoryRouter>
    );
    expect(screen.getByText(/login page/i)).toBeInTheDocument();
  });

  test("renders dashboard index (DashboardCards)", () => {
    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <AppRoutes useBrowserRouter={false} />
      </MemoryRouter>
    );
    expect(screen.getByText(/dashboard cards/i)).toBeInTheDocument();
  });

  test("redirects unknown routes to landing page", () => {
    render(
      <MemoryRouter initialEntries={["/unknown"]}>
        <AppRoutes useBrowserRouter={false} />
      </MemoryRouter>
    );
    expect(screen.getByText(/landing page/i)).toBeInTheDocument();
  });
});
