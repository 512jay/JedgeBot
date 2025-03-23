/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../App";

// Mock pages used in routes
vi.mock("../pages/Landing", () => () => <div>Landing Page</div>);
vi.mock("../pages/Login", () => () => <div>Login Page</div>);
vi.mock("../pages/Register", () => () => <div>Register Page</div>);
vi.mock("../pages/ForgotPassword", () => () => <div>Forgot Password</div>);
vi.mock("../pages/ResetPassword", () => () => <div>Reset Password</div>);
vi.mock("../pages/Dashboard", () => () => <div>Dashboard Layout</div>);

describe("App routing", () => {
  test("renders landing page by default", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText(/landing page/i)).toBeInTheDocument();
  });

  test("renders login page on /login", () => {
    render(
      <MemoryRouter initialEntries={["/login"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText(/login page/i)).toBeInTheDocument();
  });

  test("renders register page on /register", () => {
    render(
      <MemoryRouter initialEntries={["/register"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText(/register page/i)).toBeInTheDocument();
  });

  test("redirects unknown route to landing page", () => {
    render(
      <MemoryRouter initialEntries={["/not-a-real-page"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText(/landing page/i)).toBeInTheDocument();
  });
});
