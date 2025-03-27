// /frontend/src/__tests__/Login.test.jsx
/// <reference types="vitest" />

beforeAll(() => {
  global.IntersectionObserver = class {
    constructor(callback) {}
    observe() {}
    unobserve() {}
    disconnect() {}
  };
});

import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Login from "../pages/Login";
import * as authApi from "../api/auth_api";
import { AuthProvider } from "../../../context/AuthContext";

// Mock navigate function
const mockedNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockedNavigate,
  };
});

describe("Login Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  function renderWithRouter() {
    return render(
      <AuthProvider>
        <BrowserRouter>
          <Login />
        </BrowserRouter>
      </AuthProvider>
    );
  }

  test("renders email and password fields", () => {
    renderWithRouter();
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
  });

  test("updates input values", () => {
    renderWithRouter();
    const emailInput = screen.getByLabelText(/email address/i);
    const passwordInput = screen.getByLabelText(/password/i);

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "secret" } });

    expect(emailInput.value).toBe("test@example.com");
    expect(passwordInput.value).toBe("secret");
  });

  test("calls login and navigates on success", async () => {
    const mockUser = { email: "test@example.com", role: "client" };
    vi.spyOn(authApi, "login").mockResolvedValue({
      message: "Login successful",
      user: mockUser,
    });

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() =>
      expect(authApi.login).toHaveBeenCalledWith("test@example.com", "password123")
    );
    expect(mockedNavigate).toHaveBeenCalledWith("/dashboard");
  });

  test("shows error on invalid credentials", async () => {
    vi.spyOn(authApi, "login").mockResolvedValue({ message: "Invalid credentials" });

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "fail@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "wrongpass" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() =>
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    );
  });

  test("shows error on network failure", async () => {
    vi.spyOn(authApi, "login").mockRejectedValue(new Error("Network error"));

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() =>
      expect(screen.getByText(/login failed/i)).toBeInTheDocument()
    );
  });

  test("shows error when email is not verified", async () => {
    vi.spyOn(authApi, "login").mockRejectedValueOnce({
      detail: "Email not verified. Please check your email to verify your account.",
    });

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "unverified@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() =>
      expect(
        screen.getByText(/your email address has not been verified/i)
      ).toBeInTheDocument()
    );
  });

  test("shows resend button and sends request on click", async () => {
    vi.spyOn(authApi, "login").mockRejectedValueOnce({
      detail: "Email not verified. Please check your email to verify your account.",
    });

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          message: "Verification email has been resent. Please check your inbox.",
        }),
    });

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "unverified@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: /resend verification email/i })
      ).toBeInTheDocument()
    );

    fireEvent.click(screen.getByRole("button", { name: /resend verification email/i }));

    await waitFor(() =>
      expect(
        screen.getByText(/verification email has been resent/i)
      ).toBeInTheDocument()
    );
  });
});
