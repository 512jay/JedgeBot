// /frontend/src/__tests__/main.test.jsx

import { describe, it, expect } from "vitest";
import { screen } from "@testing-library/react";
import { renderWithProviders } from "../../test-utils/renderWithProviders";
import App from "../App";

describe("main.jsx entry point", () => {
  it("renders the App component without crashing", () => {
    renderWithProviders(<App />);
    expect(
      screen.getByText(/login|dashboard|register|welcome/i)
    ).toBeInTheDocument();
  });
});
