/// <reference types="vitest" />
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { BrowserRouter } from "react-router-dom";
import * as authApi from "../api/auth_api";
import Register from "../pages/Register";

// Mock useNavigate
const mockedNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockedNavigate,
  };
});

// Mock window.alert
vi.spyOn(window, "alert").mockImplementation(() => {});

describe("Register Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  function renderWithRouter() {
    render(
      <BrowserRouter>
        <Register />
      </BrowserRouter>
    );
  }

  test("renders registration form", () => {
    renderWithRouter();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument(); // 🔧
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/select role/i)).toBeInTheDocument();
  });

  test("shows error when passwords do not match", async () => {
    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" }, // 🔧
    });
    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "password123" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "notthesame" },
    });

    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(
        screen.getByText((content) => content.includes("Passwords do not match")) // 🔧
      ).toBeInTheDocument();
    });
  });

  test("registers successfully and navigates to login", async () => {
    vi.spyOn(authApi, "register").mockResolvedValue({});

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/select role/i), {
      target: { value: "client" },
    });
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "clientbot" }, // 🔧
    });
    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "abc12345" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "abc12345" },
    });

    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => expect(authApi.register).toHaveBeenCalled());
    expect(mockedNavigate).toHaveBeenCalledWith("/login");
    expect(window.alert).toHaveBeenCalledWith("Registration successful! Please log in.");
  });

  test("shows error if registration fails", async () => {
    vi.spyOn(authApi, "register").mockRejectedValue(new Error("Server error"));

    renderWithRouter();

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "failbot" }, // 🔧
    });
    fireEvent.change(screen.getByLabelText(/email address/i), {
      target: { value: "fail@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "password" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "password" },
    });

    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() =>
      expect(
        screen.getByText((content) => content.toLowerCase().includes("registration failed")) // 🔧
      ).toBeInTheDocument()
    );
  });
});
