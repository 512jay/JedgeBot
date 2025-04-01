// /frontend/vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    include: ['src/**/*.{test,spec}.{js,jsx,ts,tsx}'],
    exclude: [
      'node_modules',
      'dist',
      '.next',
      'build',
      'scripts',
      'test-utils',
      '**/*.bak.{js,ts,jsx,tsx}',
    ],
    coverage: {
      reporter: ['text', 'json', 'html'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@feat': path.resolve(__dirname, './src/features'),
      '@auth': path.resolve(__dirname, './src/features/auth'),
      '@images': path.resolve(__dirname, './src/images'),
      '@styles': path.resolve(__dirname, './src/styles'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@useAuth': path.resolve(__dirname, './src/context/useAuth'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
    },
  },
});
