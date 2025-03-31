// /frontend/src/features/landing/__tests__/WaitlistForm.test.jsx
/// <reference types="vitest" />
/* eslint-env vitest */
// Tests client-side validation and honeypot logic for WaitlistForm.

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import WaitlistForm from "../WaitlistForm";
import { vi } from "vitest";

describe("WaitlistForm", () => {
  beforeEach(() => {
    vi.resetAllMocks();
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ message: "Success" }),
      })
    );
  });

  it("renders required form fields", () => {
    render(<WaitlistForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/role/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/feedback/i)).toBeInTheDocument();
  });

  it("shows validation errors when required fields are empty", async () => {
    render(<WaitlistForm />);
    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));

    expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
    expect(await screen.findByText(/select a role/i)).toBeInTheDocument();
    expect(await screen.findByText(/at least 10 characters/i)).toBeInTheDocument();
  });

  it("prevents submission if honeypot field is filled (bot detection)", async () => {
    render(<WaitlistForm />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "bot@spam.com" },
    });
    fireEvent.change(screen.getByLabelText(/role/i), {
      target: { value: "client" },
    });
    fireEvent.change(screen.getByLabelText(/feedback/i), {
      target: { value: "This is a test bot entry" },
    });
    fireEvent.change(screen.getByLabelText(/company website/i), {
      target: { value: "http://spammybot.com" },
    });

    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));

    await waitFor(() => {
      expect(global.fetch).not.toHaveBeenCalled();
    });
  });

  it("submits successfully when all fields are valid and honeypot is empty", async () => {
    render(<WaitlistForm />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "user@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/role/i), {
      target: { value: "manager" },
    });
    fireEvent.change(screen.getByLabelText(/feedback/i), {
      target: { value: "Excited to try Fordis Ludus!" },
    });

    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    // Check that the form was cleared (email input is empty again)
    expect(screen.getByLabelText(/email/i)).toHaveValue("");
  });

  it("displays an error when the server returns failure", async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ error: "Bad request" }),
      })
    );

    render(<WaitlistForm />);
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "fail@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/role/i), {
      target: { value: "trader" },
    });
    fireEvent.change(screen.getByLabelText(/feedback/i), {
      target: { value: "Some feedback text." },
    });

    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
    });

    expect(await screen.findByText(/submission failed/i)).toBeInTheDocument();
  });
});
