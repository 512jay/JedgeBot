// /frontend/src/features/auth/__tests__/Login.test.jsx
// Unit tests for Login.jsx using Vitest + React Testing Library

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  render,
  screen,
  fireEvent,
  waitFor,
} from "@testing-library/react";
import { HelmetProvider } from "react-helmet-async";
import { BrowserRouter } from "react-router-dom";
import Login from "../Login";

// Mock login API
vi.mock("@auth/auth_api", () => ({
  login: vi.fn(),
}));

// Mock AuthContext
vi.mock("@/context/AuthContext", () => ({
  useAuth: () => ({ setUser: vi.fn() }),
}));

// Mock navigate
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

import { login } from "@auth/auth_api";

function renderWithProviders() {
  return render(
    <HelmetProvider>
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    </HelmetProvider>
  );
}

describe("Login.jsx", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the form correctly", () => {
    renderWithProviders();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
  });

  it("submits the form and navigates on successful login", async () => {
    login.mockResolvedValueOnce({
      message: "Login successful",
      user: { id: 1, email: "test@example.com" },
    });

    renderWithProviders();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith("/dashboard");
    });
  });

  it("shows error on failed login", async () => {
    login.mockRejectedValueOnce({
      response: { data: { detail: "Invalid credentials" } },
    });

    renderWithProviders();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "wrong@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "wrongpass" },
    });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });

  it("shows resend button if email is not verified", async () => {
    login.mockRejectedValueOnce({
      response: {
        data: {
          detail:
            "Your email address has not been verified. Please check your inbox for the verification email.",
        },
      },
    });

    renderWithProviders();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "verify@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    const resendBtn = await screen.findByTestId("resend-btn");
    expect(resendBtn).toBeInTheDocument();
  });

  it("includes navigation links to forgot password and register", () => {
    renderWithProviders();
    expect(
      screen.getByRole("link", { name: /forgot your password/i })
    ).toHaveAttribute("href", "/forgot-password");
    expect(
      screen.getByRole("link", { name: /register here/i })
    ).toHaveAttribute("href", "/register");
  });
});