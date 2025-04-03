// /frontend/src/routes/routes.js
// Centralized route path constants for the app

export const ROUTES = {
  // 🌐 System routes
  NOT_FOUND: "*", // Catch-all route for 404 page

  // 🏠 Public pages (marketing/information)
  HOME: "/",              // Landing page
  ABOUT: "/about",        // About the product or team
  PRICING: "/pricing",    // Pricing information
  CONTACT: "/contact",    // Public contact form

  // 🔐 Authentication routes
  LOGIN: "/login",                             // Sign-in form
  REGISTER: "/register",                       // Create a new account
  FORGOT_PASSWORD: "/forgot-password",         // Request password reset email
  SET_NEW_PASSWORD: "/reset-password",         // Form to set a new password via token
  VERIFY_EMAIL: "/verify-email",               // Link from email verification
  RESEND_VERIFICATION: "/resend-verification", // Form to resend verification email

  // 📦 Authenticated application routes
  DASHBOARD: "/dashboard", // Main user dashboard
  PROFILE: "/profile",     // Account/profile settings

  // 🧪 Internal test/dev routes
  TEST: "/test-centering", // Page for testing visual centering
  SMOKE: "/smoke",         // Smoke test route for internal checks
};
