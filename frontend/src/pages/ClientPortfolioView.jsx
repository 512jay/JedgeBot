import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Card, { CardContent } from "../components/ui/Card";
import Button from "../components/ui/Button";
import { Line } from "react-chartjs-2";
import { Pie } from "react-chartjs-2";
import "chart.js/auto";
import "../styles/ClientPortfolioView.css";

const ClientPortfolioView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [clientData, setClientData] = useState(null);

  useEffect(() => {
    // Mock API call to fetch client data
    const fetchClientData = async () => {
      const mockData = {
        name: "John Doe",
        tags: ["Aggressive Growth", "Income-Oriented"],
        totalPortfolioValue: 250000,
        performance: [100000, 120000, 140000, 180000, 200000, 220000, 250000],
        riskScore: 75,
        accounts: [
          { broker: "TastyTrade", name: "IRA", value: 80000, unrealizedPL: 5000, buyingPower: 20000, openPositions: 5 },
          { broker: "IBKR", name: "Margin", value: 120000, unrealizedPL: -2000, buyingPower: 50000, openPositions: 8 },
          { broker: "MT5", name: "Cash", value: 50000, unrealizedPL: 1000, buyingPower: 10000, openPositions: 2 }
        ],
        alerts: {
          upcomingDividends: [{ stock: "AAPL", amount: "$100" }],
          expiringOptions: [{ contract: "SPY 450C", expiration: "03/20/2025" }],
          riskExposure: { stocks: 50, bonds: 20, options: 20, crypto: 10 },
          recentTrades: [{ symbol: "TSLA", action: "Buy", quantity: 10, price: 800 }]
        }
      };
      setClientData(mockData);
    };
    fetchClientData();
  }, [id]);

  if (!clientData) return <p>Loading...</p>;

  return (
    <div className="client-portfolio-container">
      <h2>Client Portfolio: {clientData.name}</h2>
      <p>Tags: {clientData.tags.join(", ")}</p>
      <Card>
        <CardContent>
          <p>Total Portfolio Value: ${clientData.totalPortfolioValue.toLocaleString()}</p>
          <p>Risk Score: {clientData.riskScore}</p>
          <Line data={{
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
            datasets: [{
              label: "Performance Over Time",
              data: clientData.performance,
              borderColor: "blue",
              fill: false
            }]
          }} />
        </CardContent>
      </Card>
      <h3>Account Breakdown</h3>
      <table>
        <thead>
          <tr>
            <th>Broker</th>
            <th>Account Name</th>
            <th>Current Value</th>
            <th>Unrealized P/L</th>
            <th>Buying Power</th>
            <th>Open Positions</th>
          </tr>
        </thead>
        <tbody>
          {clientData.accounts.map((account, index) => (
            <tr key={index} onClick={() => navigate(`/account/${index}`)}>
              <td>{account.broker}</td>
              <td>{account.name}</td>
              <td>${account.value.toLocaleString()}</td>
              <td>${account.unrealizedPL.toLocaleString()}</td>
              <td>${account.buyingPower.toLocaleString()}</td>
              <td>{account.openPositions}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>Client-Specific Alerts & Insights</h3>
      <p>Upcoming Dividends: {clientData.alerts.upcomingDividends.map(div => `${div.stock}: ${div.amount}`).join(", ")}</p>
      <p>Expiring Options: {clientData.alerts.expiringOptions.map(opt => `${opt.contract} (Expires: ${opt.expiration})`).join(", ")}</p>
      <Pie data={{
        labels: ["Stocks", "Bonds", "Options", "Crypto"],
        datasets: [{
          data: Object.values(clientData.alerts.riskExposure),
          backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
        }]
      }} />
      <h4>Recent Trades</h4>
      <ul>
        {clientData.alerts.recentTrades.map((trade, index) => (
          <li key={index}>{trade.action} {trade.quantity} shares of {trade.symbol} at ${trade.price}</li>
        ))}
      </ul>
    </div>
  );
};

export default ClientPortfolioView;
