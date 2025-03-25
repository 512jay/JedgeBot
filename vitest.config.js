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
      '~test-utils': path.resolve(__dirname, 'frontend/test-utils'), // ✅ FIXED
    },

  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./frontend/src/test-utils/setup.js'],
    include: [
    'frontend/src/**/*.{test,spec}.{js,jsx}',
    'frontend/test-utils/**/*.{test,spec}.{js,jsx}'
    ], // ✅ supports .test.js
  },
  coverage: {
    exclude: ['tailwind.config.js'],
},

});
