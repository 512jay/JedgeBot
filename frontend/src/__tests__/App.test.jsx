/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import App from "../App";

describe("App", () => {
  test("renders without crashing", () => {
    render(<App />);
    expect(screen.getByRole("alert")).toBeInTheDocument(); // ToastContainer renders as role="alert"
  });
});
