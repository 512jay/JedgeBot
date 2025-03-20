// vite.config.js
// Configuration file for Vite, a build tool that aims to provide a faster and leaner development experience for modern web projects.

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/auth': {
        target: 'http://localhost:8000', // FastAPI backend
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
