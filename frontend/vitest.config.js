// /frontend/vitest.config.js
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { alias } from "./alias.config.js";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: './src/test-utils/vitest.setup.js',
    include: ["src/**/*.{test,spec}.{js,jsx,ts,tsx}"],
    exclude: [
      "node_modules",
      "dist",
      ".next",
      "build",
      "scripts",
      "test-utils",
      "**/*.bak.{js,ts,jsx,tsx}",
    ],
    coverage: {
      reporter: ["text", "json", "html"],
    },
  },
  resolve: {
    alias,
  },
});
