// /frontend/pages/Dashboard.jsx
import React from "react";
import Sidebar from "../components/layout/Sidebar";
import { MDBContainer } from "mdb-react-ui-kit";

const Dashboard = () => {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />

      <main className="flex-1 overflow-y-auto bg-cornflowerBlue p-6 text-white">
        <h1 className="text-4xl font-bold mb-6">Welcome to your dashboard</h1>

        <MDBContainer className="bg-white text-black rounded shadow p-4 mb-6">
          <h2 className="text-xl font-semibold mb-2">Portfolio Overview</h2>
          <p>Total Balance: $125,000</p>
          <p>Net P&L: +5.2%</p>
        </MDBContainer>

        <MDBContainer className="bg-white text-black rounded shadow p-4 mb-6">
          <h2 className="text-xl font-semibold mb-2">Recent Activity</h2>
          <ul className="list-disc list-inside">
            <li>Executed order: 100 shares of AAPL</li>
            <li>New client added: John Doe</li>
            <li>Portfolio rebalanced</li>
          </ul>
        </MDBContainer>

        <MDBContainer className="bg-white text-black rounded shadow p-4">
          <h2 className="text-xl font-semibold mb-2">Market Insights</h2>
          <p>S&P 500: +1.8%</p>
          <p>Top Gainer: TSLA +7.4%</p>
        </MDBContainer>
      </main>
    </div>
  );
};

export default Dashboard;
