/// <reference types="vitest" />
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import ResetPassword from "../pages/ResetPassword";

// Mock token in query string
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useSearchParams: () => [
      new URLSearchParams("token=mocked-token"),
    ],
    useNavigate: () => vi.fn(),
  };
});

describe("ResetPassword Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("shows loading initially", () => {
    render(
      <BrowserRouter>
        <ResetPassword />
      </BrowserRouter>
    );
    expect(screen.getByText(/checking your reset link/i)).toBeInTheDocument();
  });

  test("shows error if token is invalid", async () => {
    vi.stubGlobal("fetch", vi.fn(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ detail: "Token is invalid or expired." }),
      })
    ));

    render(
      <BrowserRouter>
        <ResetPassword />
      </BrowserRouter>
    );

    await waitFor(() =>
      expect(screen.getByText(/token is invalid or expired/i)).toBeInTheDocument()
    );
  });

  test("shows reset form if token is valid", async () => {
    vi.stubGlobal("fetch", vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
    ));

    render(
      <BrowserRouter>
        <ResetPassword />
      </BrowserRouter>
    );

    await waitFor(() =>
      expect(screen.getByLabelText(/new password/i)).toBeInTheDocument()
    );
  });

  test("shows success message on password reset", async () => {
    vi.stubGlobal("fetch", vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({}) }) // validate token
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({}) }) // reset password
    );

    render(
      <BrowserRouter>
        <ResetPassword />
      </BrowserRouter>
    );

    await waitFor(() =>
      expect(screen.getByLabelText(/new password/i)).toBeInTheDocument()
    );

    fireEvent.change(screen.getByLabelText(/new password/i), {
      target: { value: "newStrongPassword" },
    });
    fireEvent.click(screen.getByRole("button", { name: /reset password/i }));

    await waitFor(() =>
      expect(screen.getByText(/redirecting to login/i)).toBeInTheDocument()
    );
  });

  test("shows error on reset failure", async () => {
    vi.stubGlobal("fetch", vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({}) }) // validate token
      .mockResolvedValueOnce({
        ok: false,
        json: () => Promise.resolve({ detail: "Reset failed." }),
      })
    );

    render(
      <BrowserRouter>
        <ResetPassword />
      </BrowserRouter>
    );

    await waitFor(() =>
      expect(screen.getByLabelText(/new password/i)).toBeInTheDocument()
    );

    fireEvent.change(screen.getByLabelText(/new password/i), {
      target: { value: "weak" },
    });
    fireEvent.click(screen.getByRole("button", { name: /reset password/i }));

    await waitFor(() =>
      expect(screen.getByText(/reset failed/i)).toBeInTheDocument()
    );
  });
});
