// /frontend/vitest.config.js
import { defineConfig } from 'vitest/config';
import viteConfigFn from './vite.config.js';

const viteConfig = await viteConfigFn({ mode: 'test' });

export default defineConfig({
  ...viteConfig,
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test-utils/setup.js'],
    include: [
      'src/**/*.{test,spec}.{js,jsx}',
      'test-utils/**/*.{test,spec}.{js,jsx}',
    ],
  },
  coverage: {
    exclude: ['tailwind.config.js'],
  },
});
