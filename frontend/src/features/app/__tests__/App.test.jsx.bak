/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import App from "@feat/app/App";

describe("App", () => {
  test("renders without crashing and includes ToastContainer", () => {
    render(<App />);
    const toastContainer = screen.getByLabelText(/notifications/i);
    expect(toastContainer).toBeInTheDocument();
    });
});
