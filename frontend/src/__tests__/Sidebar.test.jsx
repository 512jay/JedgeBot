/// <reference types="vitest" />
import { render, screen, fireEvent } from "@testing-library/react";
import Sidebar from "../components/Sidebar";
import { BrowserRouter } from "react-router-dom";

// Mocks
const mockedNavigate = vi.fn();
const mockedReload = vi.fn();
const onAddClientMock = vi.fn();

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockedNavigate,
  };
});

describe("Sidebar Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.setItem("access_token", "mocked_token");

    // mock window.location.reload
    Object.defineProperty(window, "location", {
      writable: true,
      value: { ...window.location, reload: mockedReload },
    });
  });

  function renderSidebar() {
    render(
      <BrowserRouter>
        <Sidebar onAddClient={onAddClientMock} />
      </BrowserRouter>
    );
  }

  test("renders all navigation links and buttons", () => {
    renderSidebar();

    const links = [
      /dashboard/i,
      /accounts/i,
      /clients/i,
      /markets/i,
      /settings/i,
    ];

    for (const label of links) {
      expect(screen.getByText(label)).toBeInTheDocument();
    }

    expect(screen.getByRole("button", { name: /new client/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /logout/i })).toBeInTheDocument();
  });

  test("calls onAddClient when 'New Client' is clicked", () => {
    renderSidebar();
    const newClientBtn = screen.getByRole("button", { name: /new client/i });
    fireEvent.click(newClientBtn);
    expect(onAddClientMock).toHaveBeenCalled();
  });

  test("handles logout correctly", () => {
    renderSidebar();
    const logoutBtn = screen.getByRole("button", { name: /logout/i });
    fireEvent.click(logoutBtn);

    expect(localStorage.getItem("access_token")).toBeNull();
    expect(mockedNavigate).toHaveBeenCalledWith("/login");
    expect(mockedReload).toHaveBeenCalled();
  });

  test("toggles collapse state", () => {
    renderSidebar();

    const toggleBtn = screen.getByRole("button", { name: "" }); // The collapse button has no text
    fireEvent.click(toggleBtn);

    // After one click, sidebar should have class "collapsed"
    const sidebar = screen.getByRole("navigation", { name: /main sidebar/i });
    expect(sidebar).toHaveClass("collapsed");
  });
});
