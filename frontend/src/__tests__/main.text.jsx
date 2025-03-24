// /frontend/src/__tests__/main.test.jsx

import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "../App";
import { renderWithProviders } from "../test-utils/renderWithProviders";

describe("main.jsx entry point", () => {
  it("renders the App component without crashing", () => {
    renderWithProviders(<App />);
    expect(
      screen.getByText(/login|dashboard|register|welcome/i)
    ).toBeInTheDocument();
  });
});
