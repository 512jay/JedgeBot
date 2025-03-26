// /frontend/src/routes/AppRoutes.jsx
import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import Dashboard from "../features/dashboard/Dashboard";
import ForgotPassword from "../features/auth/ForgotPassword";
import Landing from "../features/landing/Landing";
import Login from "../features/auth/Login";
import Register from "../features/auth/Register";
import ResetPassword from "../features/auth/ResetPassword";

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
      <Route path="/dashboard" element={<Dashboard />} />

      {/* Redirect unknown routes to home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );

  return useBrowserRouter ? <BrowserRouter>{routes}</BrowserRouter> : routes;
}
