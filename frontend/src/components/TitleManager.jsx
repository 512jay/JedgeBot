// frontend/src/components/TitleManager.jsx

import { useEffect } from "react";
import { useLocation } from "react-router-dom";

const TitleManager = () => {
  const location = useLocation();
  const username = localStorage.getItem("username") || "User";

  useEffect(() => {
    let title = "FordisLudus"; // Default tab title

    if (location.pathname === "/dashboard") {
      title = `FL ${username} Dashboard`;
    } else if (location.pathname.startsWith("/client/")) {
      const pathParts = location.pathname.split("/");
      const clientName = decodeURIComponent(pathParts[2] || "Unknown Client");
      if (pathParts[3] === "account" && pathParts[4]) {
        const accountName = decodeURIComponent(pathParts[4]);
        title = `FL:${clientName} ${accountName}`;
      } else {
        title = `FL:Client ${clientName}`;
      }
    } else if (location.pathname === "/login") {
      title = "Login - FordisLudus";
    } else if (location.pathname === "/register") {
      title = "Register - FordisLudus App";
    } else if (location.pathname === "/settings") {
      title = `FordisLudus ${username} Settings`;
    }

    document.title = title;
  }, [location, username]);

  return null; // No UI needed
};

export default TitleManager;
