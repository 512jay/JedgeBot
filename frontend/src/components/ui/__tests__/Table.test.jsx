// /frontend/src/components/ui/__tests__/Table.test.jsx
/// <reference types="vitest" />
import { render, screen, within } from "@testing-library/react";
import Table from "../Table";

describe("Table Component", () => {
  const headers = ["Name", "Age", "Location"];
  const data = [
    ["Alice", "30", "NYC"],
    ["Bob", "25", "LA"],
  ];

  test("renders headers", () => {
    render(<Table headers={headers} data={[]} />);
    headers.forEach(header => {
      expect(screen.getByText(header)).toBeInTheDocument();
    });
  });

  test("renders row data", () => {
    render(<Table headers={headers} data={data} />);
    data.forEach(row => {
      row.forEach(cell => {
        expect(screen.getByText(cell)).toBeInTheDocument();
      });
    });
  });

  test("renders correct number of rows", () => {
    render(<Table headers={headers} data={data} />);
    const rows = screen.getAllByRole("row");
    // 1 header row + 2 data rows
    expect(rows.length).toBe(3);
  });

  test("handles empty data", () => {
    render(<Table headers={headers} data={[]} />);
    const rows = screen.getAllByRole("row");
    expect(rows.length).toBe(1); // header only
  });

  test("renders table cells in correct order", () => {
    render(<Table headers={headers} data={data} />);
    const row = screen.getAllByRole("row")[1]; // first data row
    const cells = within(row).getAllByRole("cell");
    expect(cells[0]).toHaveTextContent("Alice");
    expect(cells[1]).toHaveTextContent("30");
    expect(cells[2]).toHaveTextContent("NYC");
  });
});
