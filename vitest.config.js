/// <reference types="vitest" />
import { defineConfig } from 'vite'; // ✅ <== This is missing
import react from '@vitejs/plugin-react';

export default defineConfig({
  root: 'frontend',
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./test-utils/setup.js'], // ✅ Handles IntersectionObserver
  },
});

