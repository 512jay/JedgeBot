// /frontend/src/features/auth/__tests__/Register.test.jsx
// Tests for the Register.jsx form component

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { HelmetProvider } from "react-helmet-async";
import { BrowserRouter } from "react-router-dom";
import Register from "../Register";

vi.mock("@auth/auth_api", () => ({
  register: vi.fn(),
}));

vi.mock("@/context/AuthContext", () => ({
  useAuth: () => ({ setUser: vi.fn() }),
}));

const mockNavigate = vi.fn();
vi.mock("react-router-dom", async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

import { register } from "@auth/auth_api";

function renderWithProviders() {
  return render(
    <HelmetProvider>
      <BrowserRouter>
        <Register />
      </BrowserRouter>
    </HelmetProvider>
  );
}

describe("Register.jsx", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders form inputs and buttons", () => {
    renderWithProviders();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getAllByLabelText(/password/i)).toHaveLength(2);
    expect(screen.getByTestId("register-btn")).toBeInTheDocument();
  });

  it("validates password match", async () => {
    renderWithProviders();
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "123456" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "654321" },
    });
    fireEvent.click(screen.getByTestId("register-btn"));

    expect(await screen.findByTestId("registration-error"))
      .toHaveTextContent(/passwords do not match/i);
  });

  it("validates password length", async () => {
    renderWithProviders();
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "123" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "123" },
    });
    fireEvent.click(screen.getByTestId("register-btn"));

    expect(await screen.findByTestId("registration-error"))
      .toHaveTextContent(/password must be at least 6 characters/i);
  });

  it("shows error on failed registration", async () => {
    register.mockRejectedValueOnce({ detail: "Email already in use" });
    renderWithProviders();

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "existinguser" },
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "used@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "123456" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "123456" },
    });

    fireEvent.click(screen.getByTestId("register-btn"));

    expect(await screen.findByTestId("registration-error")).toBeInTheDocument();
  });

    it("navigates to login on successful registration", async () => {
    vi.useFakeTimers(); // 🔁 Move this to the top!

    register.mockResolvedValueOnce({ message: "Registration successful" });
    renderWithProviders();

    fireEvent.change(screen.getByLabelText(/username/i), {
        target: { value: "newuser" },
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
        target: { value: "new@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/^password$/i), {
        target: { value: "123456" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
        target: { value: "123456" },
    });

    fireEvent.click(screen.getByTestId("register-btn"));

    await waitFor(() => {
        expect(screen.queryByTestId("registration-error")).not.toBeInTheDocument();
    });

    // 🔁 Advance timers *after* ensuring no error
    vi.runAllTimers();

    expect(mockNavigate).toHaveBeenCalledWith("/login");

    vi.useRealTimers(); // cleanup
    });

});