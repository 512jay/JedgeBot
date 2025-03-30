/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Landing from "../pages/Landing";

describe("Landing Page", () => {
  function renderPage() {
    render(
      <BrowserRouter>
        <Landing />
      </BrowserRouter>
    );
  }

  test("renders navbar with expected links", () => {
    renderPage();

    const links = [
      /about/i,
      /pricing/i,
      /how it works/i,
      /login/i,
    ];

    for (const label of links) {
      expect(screen.getByRole("link", { name: label })).toBeInTheDocument();
    }

    // Navbar Sign Up button (small)
    const navButtons = screen.getAllByRole("button", { name: /sign up/i });
    expect(navButtons[0]).toBeInTheDocument();
  });

  test("renders hero card content", () => {
    renderPage();

    expect(
      screen.getByRole("heading", { name: /welcome to jedgebot/i })
    ).toBeInTheDocument();

    expect(
      screen.getByText(/your ultimate trading automation/i)
    ).toBeInTheDocument();

    const heroButtons = screen.getAllByRole("button", { name: /sign up/i });
    const loginButton = screen.getByRole("button", { name: /login/i });

    expect(loginButton).toBeInTheDocument();
    expect(heroButtons.length).toBeGreaterThanOrEqual(2); // Navbar + Hero
  });

  test("includes hero image", () => {
    renderPage();

    const image = screen.getByAltText(/jedgebot/i);
    expect(image).toBeInTheDocument();
    expect(image.getAttribute("src")).toContain("welcomejedgebot");
  });
});
