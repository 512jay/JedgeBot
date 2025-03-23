// /frontend/src/components/TitleManager.jsx

import { useEffect } from "react";
import { useLocation } from "react-router-dom";

const TitleManager = () => {
  const location = useLocation();
  const username = localStorage.getItem("username") || "User";

  const titlesByRoute = {
    "/dashboard": () => `FL ${username} Dashboard`,
    "/login": () => "Login - FordisLudus",
    "/register": () => "Register - FordisLudus App",
    "/settings": () => `FordisLudus ${username} Settings`,
  };

  const computeTitle = () => {
    const path = location.pathname;

    if (titlesByRoute[path]) {
      return titlesByRoute[path]();
    }

    if (path.startsWith("/client/")) {
      const [, , clientSlug, section, accountSlug] = path.split("/");
      const clientName = decodeURIComponent(clientSlug || "Unknown Client");

      if (section === "account" && accountSlug) {
        const accountName = decodeURIComponent(accountSlug);
        return `FL:${clientName} ${accountName}`;
      }

      return `FL:Client ${clientName}`;
    }

    return "FordisLudus";
  };

  useEffect(() => {
    document.title = computeTitle();
  }, [location, username]);

  return null;
};

export default TitleManager;
