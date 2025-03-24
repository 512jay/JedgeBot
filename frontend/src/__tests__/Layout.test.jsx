import { render, screen } from "@testing-library/react";
import App from "@/App";

test("renders Navbar and Sidebar in full layout", () => {
  render(<App />);
  expect(screen.getByText(/jedgebot dashboard/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /logout/i })).toBeInTheDocument();
});
