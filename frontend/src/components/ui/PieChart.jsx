import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChart = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.sector),
    datasets: [
      {
        data: data.map(item => item.percentage),
        backgroundColor: ["#4CAF50", "#2196F3", "#FF9800", "#E91E63"],
      },
    ],
  };

  return (
    <div className="w-64 h-64">
      <Pie data={chartData} />
    </div>
  );
};

export default PieChart;
