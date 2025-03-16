import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Line, Pie } from "react-chartjs-2";
import "chart.js/auto";
import Card, { CardContent } from "../components/ui/Card";
import Button from "../components/ui/Button";
import "../styles/AccountLevelView.css";

const AccountLevelView = () => {
  const { id } = useParams();
  const [accountData, setAccountData] = useState(null);

  useEffect(() => {
    // Mock API call to fetch account-level data
    const fetchAccountData = async () => {
      const mockData = {
        broker: "TastyTrade",
        accountType: "Margin",
        buyingPower: 50000,
        marginUtilization: 45,
        cashAvailable: 25000,
        holdings: [
          { symbol: "AAPL", type: "Stock", quantity: 50, pl: 1200, change: 5 },
          { symbol: "TSLA", type: "Stock", quantity: 30, pl: -800, change: -3 },
          { symbol: "SPY 450C", type: "Option", quantity: 10, pl: 600, change: 8 },
        ],
        tradeHistory: [
          { time: "10:15 AM", symbol: "AAPL", action: "Buy", quantity: 10, price: 180 },
          { time: "12:30 PM", symbol: "TSLA", action: "Sell", quantity: 5, price: 750 },
        ],
        riskManagement: {
          stopLoss: "Enabled",
          drawdownProtection: "Active",
          volatilityAlert: "High",
        },
      };
      setAccountData(mockData);
    };
    fetchAccountData();
  }, [id]);

  if (!accountData) return <p>Loading account details...</p>;

  return (
    <div className="account-level-container">
      <h2>Account Overview: {accountData.broker} ({accountData.accountType})</h2>
      <Card>
        <CardContent>
          <p><strong>Buying Power:</strong> ${accountData.buyingPower.toLocaleString()}</p>
          <p><strong>Margin Utilization:</strong> {accountData.marginUtilization}%</p>
          <p><strong>Cash Available:</strong> ${accountData.cashAvailable.toLocaleString()}</p>
        </CardContent>
      </Card>
      
      <h3>Live Portfolio Data</h3>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Type</th>
            <th>Quantity</th>
            <th>P/L</th>
            <th>% Change</th>
          </tr>
        </thead>
        <tbody>
          {accountData.holdings.map((holding, index) => (
            <tr key={index}>
              <td>{holding.symbol}</td>
              <td>{holding.type}</td>
              <td>{holding.quantity}</td>
              <td>${holding.pl.toLocaleString()}</td>
              <td>{holding.change}%</td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <h3>Trade Execution</h3>
      <Button>Execute Trade</Button>
      
      <h3>Trade History</h3>
      <ul>
        {accountData.tradeHistory.map((trade, index) => (
          <li key={index}>{trade.time} - {trade.action} {trade.quantity} of {trade.symbol} @ ${trade.price}</li>
        ))}
      </ul>
      
      <h3>Risk Management</h3>
      <p><strong>Stop Loss:</strong> {accountData.riskManagement.stopLoss}</p>
      <p><strong>Drawdown Protection:</strong> {accountData.riskManagement.drawdownProtection}</p>
      <p><strong>Volatility Alerts:</strong> {accountData.riskManagement.volatilityAlert}</p>
    </div>
  );
};

export default AccountLevelView;
