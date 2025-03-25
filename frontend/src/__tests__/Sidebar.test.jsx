// /frontend/src/__tests__/Sidebar.test.jsx
import { render, screen, fireEvent } from "@testing-library/react";
import Sidebar from "@/components/layout/Sidebar";
import { BrowserRouter } from "react-router-dom";

describe("Sidebar Component", () => {
  const renderSidebar = () =>
    render(
      <BrowserRouter>
        <Sidebar />
      </BrowserRouter>
    );

  test("renders navigation links", () => {
    renderSidebar();
    expect(screen.getByText(/dashboard/i)).toBeInThe
