// /frontend/src/AppRoutes.jsx
import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import Dashboard from "../pages/Dashboard";
import ForgotPassword from "../pages/ForgotPassword";
import Landing from "../pages/Landing";
import Login from "../pages/Login";
import Register from "../pages/Register";
import ResetPassword from "../pages/ResetPassword";

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
