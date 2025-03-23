/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'; // ✅ ADD THIS

export default defineConfig({
  server: {
    port: 5173,
    strictPort: true,
    open: true,
  },
  base: '/',
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'frontend/src'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./frontend/test-utils/setup.js'],
    include: ['frontend/src/**/*.{test,spec}.{js,jsx}'], // ✅ supports .test.js
  },

});
