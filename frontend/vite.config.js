// /frontend/vite.config.js
/* global process */

import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

// Define __dirname manually (ESM compatible)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
        "@feat": path.resolve(__dirname, "src/features"),
        "@auth": path.resolve(__dirname, "src/features/auth"),
        "@images": path.resolve(__dirname, "public/images"),
        "@styles": path.resolve(__dirname, "src/styles"),
      },
    },
    server: {
      proxy: {
        "/auth": {
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
