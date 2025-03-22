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

/// <reference types="vitest" />
// /frontend/src/__tests__/Login.test.jsx
import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Login from "../pages/Login";
import * as authApi from "../api/auth_api";

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
      <BrowserRouter>
        <Login />
      </BrowserRouter>
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
    vi.spyOn(authApi, "login").mockResolvedValue({ message: "Login successful" });

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => expect(authApi.login).toHaveBeenCalledWith("test@example.com", "password123"));
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
});
