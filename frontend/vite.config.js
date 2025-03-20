// vite.config.js
// Configuration file for Vite, a build tool that aims to provide a faster and leaner development experience for modern web projects.

import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  // Load environment variables from `.env` file
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],
    server: {
      proxy: {
        '/auth': {
          target: env.VITE_API_URL || 'http://localhost:8000', // ✅ Fix: Use `loadEnv`
          changeOrigin: true,
          secure: false,
        },
      },
    },
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(env.VITE_API_URL || 'http://localhost:8000'),
    },
  };
});

