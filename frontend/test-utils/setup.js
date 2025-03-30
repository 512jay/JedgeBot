// /frontend/test/setup.js
import '@testing-library/jest-dom/vitest'; // ✅ Gives us `toBeInTheDocument`

global.IntersectionObserver = class {
  constructor(callback) {}
  observe() {}
  unobserve() {}
  disconnect() {}
};

