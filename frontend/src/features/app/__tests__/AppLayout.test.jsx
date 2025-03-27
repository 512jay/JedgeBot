import { render, screen } from "@testing-library/react";
import App from "@feat/app/App";

test("renders Navbar and Sidebar in full layout", () => {
  render(<App />);

  // Match the brand in the navbar
  expect(screen.getAllByText(/jedgebot/i).length).toBeGreaterThan(0);

  // Optional: match main heading
  expect(screen.getByText(/welcome to jedgebot/i)).toBeInTheDocument();

  // Check Login button
  expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
});
