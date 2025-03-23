/// <reference types="vitest" />
import { defineConfig } from 'vite'; // ✅ <== This is missing
import react from '@vitejs/plugin-react';

export default defineConfig({
  server: {
    port: 5173, // Default Vite port is 3000, you can change it if needed
    strictPort: true, // Ensures that the server will exit if the port is already in use
    open: true, // Opens the browser when the server starts
  },
  base: '/',
  // root: 'frontend',
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./frontend/test-utils/setup.js'], // ✅ Handles IntersectionObserver
  },
});

