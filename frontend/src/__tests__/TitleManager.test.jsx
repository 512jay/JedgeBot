/// <reference types="vitest" />
import { render } from "@testing-library/react";
import TitleManager from "../components/TitleManager";
import { MemoryRouter, Route, Routes } from "react-router-dom";


describe("TitleManager", () => {
  beforeEach(() => {
    localStorage.setItem("username", "TestUser");
    document.title = ""; // reset before each test
  });

  function renderWithPath(path) {
    render(
      <MemoryRouter initialEntries={[path]}>
        <Routes>
          <Route path="*" element={<TitleManager />} />
        </Routes>
      </MemoryRouter>
    );
  }

  test("sets title for /dashboard", () => {
    renderWithPath("/dashboard");
    expect(document.title).toBe("FL TestUser Dashboard");
  });

  test("sets title for /login", () => {
    renderWithPath("/login");
    expect(document.title).toBe("Login - FordisLudus");
  });

  test("sets title for /register", () => {
    renderWithPath("/register");
    expect(document.title).toBe("Register - FordisLudus App");
  });

  test("sets title for /settings", () => {
    renderWithPath("/settings");
    expect(document.title).toBe("FordisLudus TestUser Settings");
  });

  test("sets dynamic client title", () => {
    renderWithPath("/client/john-doe");
    expect(document.title).toBe("FL:Client John Doe");
  });

  test("sets dynamic client/account title", () => {
    renderWithPath("/client/john-doe/account/ABC123");
    expect(document.title).toBe("FL:John Doe ABC123");
  });

  test("sets fallback title for unknown routes", () => {
    renderWithPath("/not-a-match");
    expect(document.title).toBe("FordisLudus");
  });
});
