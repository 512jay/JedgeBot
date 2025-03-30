// /frontend/src/components/ui/__tests__/PieChart.test.jsx
import { render } from "@testing-library/react";
import PieChart from "../PieChart";

describe("PieChart", () => {
  it("renders without crashing", () => {
    render(<PieChart data={[{ name: "AAPL", value: 80 }]} />);
  });
});
