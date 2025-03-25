// /frontend/pages/Dashboard.jsx
// Dashboard layout with left sidebar and cornflower blue main area
import React from "react";
import Sidebar from "../components/layout/Sidebar";

const Dashboard = () => {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-auto p-8 transition-all duration-300 bg-cornflowerBlue ml-16 md:ml-64">
        <h1 className="text-4xl font-semibold mb-6 text-white">Welcome to your dashboard</h1>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-2">Portfolio Overview</h2>
          <p>Total Balance: $125,000</p>
          <p>Net P&L: +5.2%</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-2">Recent Activity</h2>
          <ul className="list-disc list-inside">
            <li>Executed order: 100 shares of AAPL</li>
            <li>New client added: John Doe</li>
            <li>Portfolio rebalanced</li>
          </ul>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-2">Market Insights</h2>
          <p>S&P 500: +1.8%</p>
          <p>Top Gainer: TSLA +7.4%</p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
