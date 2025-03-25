/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ForgotPassword from "../pages/ForgotPassword";

// Mock global fetch
beforeEach(() => {
  global.fetch = vi.fn();
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("ForgotPassword Page", () => {
  test("renders form elements", () => {
    render(<ForgotPassword />);
    expect(screen.getByLabelText(/enter your email address/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /request reset link/i })).toBeInTheDocument();
  });

  test("updates email input", () => {
    render(<ForgotPassword />);
    const input = screen.getByLabelText(/enter your email address/i);
    fireEvent.change(input, { target: { value: "test@example.com" } });
    expect(input.value).toBe("test@example.com");
  });

  test("shows success message on successful response", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    render(<ForgotPassword />);
    fireEvent.change(screen.getByLabelText(/enter your email address/i), {
      target: { value: "user@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: /request reset link/i }));

    await waitFor(() => {
      expect(screen.getByText(/a reset link has been sent/i)).toBeInTheDocument();
    });
  });

  test("shows error message on failure", async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: "Email not found" }),
    });

    render(<ForgotPassword />);
    fireEvent.change(screen.getByLabelText(/enter your email address/i), {
      target: { value: "invalid@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: /request reset link/i }));

    await waitFor(() => {
      expect(screen.getByText(/email not found/i)).toBeInTheDocument();
    });
  });

  test("shows generic error on network failure", async () => {
    fetch.mockRejectedValueOnce(new Error("Network error"));

    render(<ForgotPassword />);
    fireEvent.change(screen.getByLabelText(/enter your email address/i), {
      target: { value: "any@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: /request reset link/i }));

    await waitFor(() => {
      expect(screen.getByText(/unable to process/i)).toBeInTheDocument();
    });
  });
});
