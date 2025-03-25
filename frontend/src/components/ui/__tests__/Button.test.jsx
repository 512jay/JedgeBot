/// <reference types="vitest" />
import { render, screen, fireEvent } from "@testing-library/react";
import Button from "../Button";

describe("Button Component", () => {
  test("renders child text", () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByRole("button", { name: /click me/i })).toBeInTheDocument();
  });

  test("triggers onClick when clicked", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Fire</Button>);
    fireEvent.click(screen.getByRole("button", { name: /fire/i }));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test("applies custom class", () => {
    render(<Button className="custom-class">Styled</Button>);
    const button = screen.getByRole("button", { name: /styled/i });
    expect(button.className).toMatch(/custom-class/);
  });

  test("respects type prop", () => {
    render(<Button type="submit">Submit</Button>);
    const button = screen.getByRole("button", { name: /submit/i });
    expect(button).toHaveAttribute("type", "submit");
  });
});
