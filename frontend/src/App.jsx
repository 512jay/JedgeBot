// /frontend/src/App.jsx
//import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Landing from "./pages/Landing"; // Import Landing page
import Login from "./pages/Login";
import DashboardLayout from "./pages/Dashboard";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";

function App() {
  return (
    <Router>
      <Routes>
        {/* Landing Page as Default */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />

        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Home />} />
          <Route path="profile" element={<Profile />} />
          <Route path="settings" element={<Settings />} />
        </Route>

        {/* Redirect unknown routes */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
