import { Routes, Route, Navigate } from "react-router-dom";
import PublicLayout from "@/components/layouts/PublicLayout";
import DashboardLayout from "@/components/layouts/DashboardLayout";
import PrivateRoute from "@/components/routing/PrivateRoute";

// Public pages
import Landing from "@/features/landing/Landing";
import About from "@/features/landing/About";
import Pricing from "@/features/landing/Pricing";
import Contact from "@/features/landing/Contact";
import NotFound from "@/features/app/pages/NotFound";


// Auth pages
import Login from "@/features/auth/Login";
import Register from "@/features/auth/Register";
import ForgotPassword from "@/features/auth/ForgotPassword";
import ResetPassword from "@/features/auth/ResetPassword";
import VerifyEmail from "@/features/auth/VerifyEmail";

// Dashboard feature entry
import Dashboard from "@/features/dashboard/Dashboard";

export default function AppRoutes() {
  return (
    <Routes>

      {/* 🌐 Public-facing layout */}
      <Route element={<PublicLayout />}>
        <Route path="/" element={<Landing />} />
        <Route path="/about" element={<About />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/contact" element={<Contact />} />

        {/* Auth-related */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/verify-email" element={<VerifyEmail />} />
      </Route>

      {/* 🔒 Dashboard - protected + layout */}
      <Route element={<PrivateRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Add more nested dashboard routes here */}
        </Route>
      </Route>

      {/* 🚫 Not Found (public) */}
      <Route path="*" element={<PublicLayout pageTitle='404 Not Found'><NotFound /></PublicLayout>} />
    </Routes>
  );
}
