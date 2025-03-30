// /frontend/src/components/TitleManager.jsx

import { useEffect } from "react";
import { useLocation } from "react-router-dom";

const titleCase = (str) =>
  str
    .split(/[\s-_]/)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");

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
      const clientName = titleCase(decodeURIComponent(clientSlug || "Unknown Client"));

      if (section === "account" && accountSlug) {
        const accountName = titleCase(decodeURIComponent(accountSlug));
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
