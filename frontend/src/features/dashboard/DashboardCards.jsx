// /frontend/src/components/DashboardCards.jsx
import { Card, CardContent } from "@/components/ui/Card";


const DashboardCards = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
      {/* Portfolio Overview */}
      <Card className="shadow-lg">
        <div className="p-6">
          <h2 className="text-xl font-semibold">Portfolio Overview</h2>
          <p className="text-gray-600">
            Total Balance: <span className="font-bold">$125,000</span>
          </p>
          <p className="text-gray-600">
            Net P&L: <span className="text-green-600">+5.2%</span>
          </p>
        </div>
      </Card>

      {/* Recent Activity */}
      <Card className="shadow-lg">
        <div className="p-6">
          <h2 className="text-xl font-semibold">Recent Activity</h2>
          <ul className="list-disc ml-4 text-gray-600">
            <li>Executed order: 100 shares of AAPL</li>
            <li>New client added: John Doe</li>
            <li>Portfolio rebalanced</li>
          </ul>
        </div>
      </Card>

      {/* Market Insights */}
      <Card className="shadow-lg">
        <div className="p-6">
          <h2 className="text-xl font-semibold">Market Insights</h2>
          <p className="text-gray-600">
            S&P 500: <span className="font-bold">+1.8%</span>
          </p>
          <p className="text-gray-600">
            Top Gainer: <span className="font-bold">TSLA +7.4%</span>
          </p>
        </div>
      </Card>
    </div>
  );
};

export default DashboardCards;
