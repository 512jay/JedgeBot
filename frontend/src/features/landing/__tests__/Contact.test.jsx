// /frontend/src/features/landing/__tests__/Contact.test.jsx

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Contact from "../Contact";
import { toast } from "react-toastify";

// 👇 mock toast globally
vi.mock("react-toastify", () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));
// Mock global fetch
beforeEach(() => {
  global.fetch = vi.fn();
});

describe("Contact Form", () => {
  it("renders the form inputs", () => {
    render(<Contact />);

    expect(screen.getByLabelText(/your email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /send message/i })).toBeInTheDocument();
  });

  it("sends a message and shows success feedback", async () => {
    fetch.mockResolvedValueOnce({ ok: true, json: () => ({ message: "Success" }) });
  
    render(<Contact />);
    fireEvent.change(screen.getByLabelText(/your email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/message/i), {
      target: { value: "Hello!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send message/i }));
  
    await waitFor(() => {
      expect(toast.success).toHaveBeenCalledWith("Your message has been sent successfully!");
    });
  });
  

  it("shows error feedback on failure", async () => {
    fetch.mockRejectedValueOnce(new Error("Network error"));
  
    render(<Contact />);
    fireEvent.change(screen.getByLabelText(/your email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/message/i), {
      target: { value: "Something went wrong" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send message/i }));
  
    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith(
        "There was a problem sending your message. Try again later."
      );
    });
  });
  
});
