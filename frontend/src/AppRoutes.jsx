// /frontend/src/AppRoutes.jsx
import {
  Routes,
  Route,
  Navigate,
  BrowserRouter,
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Landing from "./pages/Landing";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import DashboardView from "./views/DashboardView"; // ✅ updated path/name

export function AppRoutes({ useBrowserRouter = true }) {
  const routes = (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />

      {/* Role-aware Dashboard View */}
      <Route path="/dashboard" element={<DashboardView />} />

      {/* Redirect unknown routes to home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );

  return useBrowserRouter ? <BrowserRouter>{routes}</BrowserRouter> : routes;
}
