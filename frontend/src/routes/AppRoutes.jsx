// /frontend/src/routes/AppRoutes.jsx
import { Routes, Route } from "react-router-dom";
import { ROUTES } from "@/routes/routes";
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

// Dashboard
import Dashboard from "@/features/dashboard/Dashboard";

export default function AppRoutes() {
  return (
    <Routes>
      {/* 🌐 Public-facing layout */}
      <Route element={<PublicLayout />}>
        <Route path={ROUTES.HOME} element={<Landing />} />
        <Route path={ROUTES.ABOUT} element={<About />} />
        <Route path={ROUTES.PRICING} element={<Pricing />} />
        <Route path={ROUTES.CONTACT} element={<Contact />} />

        {/* Auth-related */}
        <Route path={ROUTES.LOGIN} element={<Login />} />
        <Route path={ROUTES.REGISTER} element={<Register />} />
        <Route path={ROUTES.FORGOT_PASSWORD} element={<ForgotPassword />} />
        <Route path={ROUTES.RESET_PASSWORD} element={<ResetPassword />} />
        <Route path={ROUTES.VERIFY_EMAIL} element={<VerifyEmail />} />
      </Route>

      {/* 🔒 Dashboard - protected + layout */}
      <Route element={<PrivateRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path={ROUTES.DASHBOARD} element={<Dashboard />} />
        </Route>
      </Route>

      {/* 🚫 Not Found */}
      <Route path={ROUTES.NOT_FOUND} element={
        <PublicLayout pageTitle="404 Not Found">
          <NotFound />
        </PublicLayout>
      } />
    </Routes>
  );
}
