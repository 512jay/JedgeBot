/* global process */
// /frontend/vite.config.js

import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { alias } from "./alias.config.js";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    base: mode === "production" ? "/" : undefined,
    plugins: [react()],
    resolve: {
      alias,
    },
    server: {
      host: "0.0.0.0",
      port: 5173,
      proxy: {
        "/auth": {
          target: env.VITE_API_URL || "http://localhost:8000",
          changeOrigin: true,
          secure: false,
        },
        "/api": {
          target: env.VITE_API_URL || "http://localhost:8000",
          changeOrigin: true,
          secure: false,
        },
      },
    },
    define: {
      "import.meta.env.VITE_API_URL": JSON.stringify(env.VITE_API_URL || "http://localhost:8000"),
    },
  };
});
