/// <reference types="vitest" />
// /frontend/src/features/landing/__tests__/WaitlistForm.test.jsx
// Tests client-side validation and honeypot logic for WaitlistForm.

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import WaitlistForm from "../WaitlistForm";
import { vi } from "vitest";

describe("WaitlistForm", () => {
  beforeEach(() => {
    // Clear mocks before each test
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ message: "Success" }),
      })
    );
  });

  it("renders the form fields", () => {
    render(<WaitlistForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/role/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/feedback/i)).toBeInTheDocument();
  });

  it("shows validation errors for required fields", async () => {
    render(<WaitlistForm />);
    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));

    expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
    expect(await screen.findByText(/select a role/i)).toBeInTheDocument();
    expect(await screen.findByText(/at least 10 characters/i)).toBeInTheDocument();
  });

  it("blocks bots using honeypot fields", async () => {
    render(<WaitlistForm />);

    fireEvent.input(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/role/i), {
      target: { value: "client" },
    });
    fireEvent.change(screen.getByLabelText(/feedback/i), {
      target: { value: "Very interested in your platform!" },
    });

    // Fill honeypot field
    const honeypot = screen.getByLabelText(/homepage/i);
    fireEvent.change(honeypot, { target: { value: "https://spam.com" } });

    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));

    await waitFor(() => {
      expect(global.fetch).not.toHaveBeenCalled();
    });
  });

  it("submits successfully with valid input", async () => {
    render(<WaitlistForm />);

    fireEvent.input(screen.getByLabelText(/email/i), {
      target: { value: "realuser@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/role/i), {
      target: { value: "manager" },
    });
    fireEvent.change(screen.getByLabelText(/feedback/i), {
      target: { value: "Looking forward to using Fordis Ludus!" },
    });

    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
    });

    expect(await screen.findByText(/you're on the waitlist/i)).toBeInTheDocument();
  });
});
