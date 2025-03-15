// frontend/src/App.js
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import PortfolioManagerOverview from "./pages/PortfolioManagerOverview";
import ClientPortfolioView from "./pages/ClientPortfolioView";
import AccountLevelView from "./pages/AccountLevelView";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import "./styles/Home.css";

function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("authToken"); // ✅ Check if user is logged in
    setIsAuthenticated(!!token); // Convert token presence to boolean
  }, []);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Dashboard Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <PortfolioManagerOverview />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/client/:id"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <ClientPortfolioView />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/:id"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <AccountLevelView />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

// ✅ Wrapper component to include Sidebar + Navbar in the Dashboard Views
function DashboardLayout({ children }) {
  return (
    <div className="dashboard-container d-flex">
      <Sidebar />
      <div className="main-content flex-grow-1">
        <Navbar />
        <div className="content p-4">{children}</div>
      </div>
    </div>
  );
}

export default App;
