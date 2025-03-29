// /frontend/src/components/ui/__tests__/Card.test.jsx
/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import { Card, CardContent } from "../Card";

describe("Card Component", () => {
  test("renders children", () => {
    render(<Card><p>Inside Card</p></Card>);
    expect(screen.getByText(/inside card/i)).toBeInTheDocument();
  });

  test("applies additional className", () => {
    render(<Card className="extra">Content</Card>);
    const card = screen.getByTestId("card");
    expect(card).toHaveClass("extra");
  });
});

describe("CardContent Component", () => {
  test("renders children", () => {
    render(<CardContent><span>Inside Content</span></CardContent>);
    expect(screen.getByText(/inside content/i)).toBeInTheDocument();
  });

  test("applies additional className", () => {
    render(<CardContent className="custom-padding">More</CardContent>);
    const cardContent = screen.getByTestId("card-content");
    expect(cardContent).toHaveClass("custom-padding");
  });
});
