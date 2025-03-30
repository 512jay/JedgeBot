// /frontend/src/features/auth/__tests__/ForgotPassword.test.jsx
// Tests for ForgotPassword.jsx component using Vitest + React Testing Library

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ForgotPassword from "../ForgotPassword";
import { HelmetProvider } from "react-helmet-async";

// Mock fetch
global.fetch = vi.fn();

// Wrap component with HelmetProvider for tests
const renderWithHelmet = (ui) => render(<HelmetProvider>{ui}</HelmetProvider>);

describe("ForgotPassword.jsx", () => {
  beforeEach(() => {
    fetch.mockReset();
  });

  it("renders form correctly", () => {
    renderWithHelmet(<ForgotPassword />);
    expect(screen.getByRole("heading", { name: /forgot your password/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/enter your email address/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /request reset link/i })).toBeInTheDocument();
  });

  it("disables the button while loading", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    renderWithHelmet(<ForgotPassword />);
    fireEvent.change(screen.getByLabelText(/enter your email address/i), {
      target: { value: "test@example.com" },
    });

    const button = screen.getByRole("button");
    fireEvent.click(button);

    expect(button).toBeDisabled();
    await waitFor(() => expect(button).not.toBeDisabled());
  });

  it("shows success message when request succeeds", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    renderWithHelmet(<ForgotPassword />);
    fireEvent.change(screen.getByLabelText(/enter your email address/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.click(screen.getByRole("button"));

    await waitFor(() =>
      expect(screen.getByText(/a reset link has been sent/i)).toBeInTheDocument()
    );
  });

  it("shows error message when server returns error", async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: "User not found" }),
    });

    renderWithHelmet(<ForgotPassword />);
    fireEvent.change(screen.getByLabelText(/enter your email address/i), {
      target: { value: "wrong@example.com" },
    });
    fireEvent.click(screen.getByRole("button"));

    await waitFor(() =>
      expect(screen.getByText(/user not found/i)).toBeInTheDocument()
    );
  });

  it("shows fallback error message on fetch failure", async () => {
    fetch.mockRejectedValueOnce(new Error("Network error"));

    renderWithHelmet(<ForgotPassword />);
    fireEvent.change(screen.getByLabelText(/enter your email address/i), {
      target: { value: "networkfail@example.com" },
    });
    fireEvent.click(screen.getByRole("button"));

    await waitFor(() =>
      expect(
        screen.getByText(/unable to process your request/i)
      ).toBeInTheDocument()
    );
  });

  it("has a link back to login", () => {
    renderWithHelmet(<ForgotPassword />);
    const link = screen.getByRole("link", { name: /back to login/i });
    expect(link).toHaveAttribute("href", "/login");
  });
});
