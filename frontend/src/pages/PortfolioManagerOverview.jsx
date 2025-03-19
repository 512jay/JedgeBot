import React, { useMemo } from "react";
import Card from "../components/ui/Card";
import Table from "../components/ui/Table";
import PieChart from "../components/ui/PieChart";
import "../styles/PortfolioManagerOverview.css";

const PortfolioManagerOverview = () => {
  console.log("✅ PortfolioManagerOverview is rendering...");

  const portfolioSummary = useMemo(() => ({
    totalValue: 1250000,
    dailyChange: 1.2,
    clients: [
      { name: "Client A", accounts: 3, value: 500000, change: "+2.5%", risk: "Low", alerts: 1 },
      { name: "Client B", accounts: 2, value: 300000, change: "-1.2%", risk: "Medium", alerts: 0 },
    ],
    bestPerformer: { name: "Client A", return: "+8.5%" },
    worstPerformer: { name: "Client C", return: "-3.2%" },
    sectorAllocation: [
      { sector: "Tech", percentage: 40 },
      { sector: "Healthcare", percentage: 25 },
      { sector: "Financials", percentage: 20 },
      { sector: "Energy", percentage: 15 },
    ],
    marketSummary: {
      sp500: "+0.8%",
      nasdaq: "-0.2%",
      dow: "+0.5%",
      vix: "18.3",
    },
    alerts: [
      { type: "Margin Call", client: "Client A" },
      { type: "Expiring Option", client: "Client B" },
    ],
  }), []);

  return (
    <div className="dashboard-container">
      <div className="aum-section">
        <Card><h3>Total AUM</h3><p>${portfolioSummary.totalValue.toLocaleString()}</p></Card>
        <Card><h3>Daily Change</h3><p className={portfolioSummary.dailyChange >= 0 ? 'text-green-500' : 'text-red-500'}>{portfolioSummary.dailyChange}%</p></Card>
      </div>
      <div className="market-summary">
        <Card>
          <h3>Market Summary</h3>
          <p>S&P 500: {portfolioSummary.marketSummary.sp500}</p>
          <p>NASDAQ: {portfolioSummary.marketSummary.nasdaq}</p>
          <p>DOW: {portfolioSummary.marketSummary.dow}</p>
          <p>VIX: {portfolioSummary.marketSummary.vix}</p>
        </Card>
      </div>
      <div className="client-table">
        <Table headers={["Client", "Accounts", "Portfolio Value", "Today's Change", "Risk Level", "Unresolved Alerts"]} 
               data={portfolioSummary.clients.map(client => [client.name, client.accounts, `$${client.value.toLocaleString()}`, client.change, client.risk, client.alerts])} />
      </div>
      <div className="alerts-section">
        <h3>Alerts & To-Do List</h3>
        <ul>
          {portfolioSummary.alerts.map((alert, index) => (
            <li key={index} className="text-red-500">{alert.type} - {alert.client}</li>
          ))}
        </ul>
      </div>
      <div className="pie-chart-container">
        <h3>Sector Allocation</h3>
        <PieChart data={portfolioSummary.sectorAllocation} />
      </div>
    </div>
  );
};

export default PortfolioManagerOverview;
