// frontend/src/App.js
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import TitleManager from "./components/TitleManager"; // ✅ Updates title dynamically
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register"
import PortfolioManagerOverview from "./pages/PortfolioManagerOverview";
import ClientPortfolioView from "./pages/ClientPortfolioView";
import AccountLevelView from "./pages/AccountLevelView";
import Clients from "./pages/Clients";  // ✅ Import Clients Page
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import "./styles/Home.css";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("access_token");

  if (!token) {
    console.log("❌ User NOT authenticated. Redirecting...");
    return <Navigate to="/login" replace />;
  }

  console.log("✅ User authenticated. Rendering page.");
  return children;
}

function App() {
  return (
    <Router>
      <TitleManager /> {/* ✅ Automatically updates the title */}
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardLayout>
              <PortfolioManagerOverview />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        {/* ✅ NEW: Clients Page Route */}
        <Route path="/clients" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Clients />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/client/:id" element={
          <ProtectedRoute>
            <DashboardLayout>
              <ClientPortfolioView />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/client/:id/account/:account_id" element={
          <ProtectedRoute>
            <DashboardLayout>
              <AccountLevelView />
            </DashboardLayout>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

// ✅ Wrapper component to include Sidebar + Navbar in the Dashboard Views
function DashboardLayout({ children }) {
  console.log("DashboardLayout: Rendering...");

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
