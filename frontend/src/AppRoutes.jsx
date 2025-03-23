// /frontend/src/AppRoutes.jsx
import {
  Routes, Route, Navigate, Outlet, BrowserRouter,
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Landing from "./pages/Landing";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import DashboardPage from "./pages/DashboardPage";

export function AppRoutes({ useBrowserRouter = true }) {
  const content = (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />

      <Route path="/dashboard" element={<DashboardPage />} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );

  return useBrowserRouter ? <BrowserRouter>{content}</BrowserRouter> : content;
}
