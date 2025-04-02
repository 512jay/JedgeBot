// /frontend/src/test-util/vitest.setup.js
// Global setup for Vitest - mocks unsupported browser features in jsdom

/* eslint-env node */
import '@testing-library/jest-dom';

global.IntersectionObserver = class IntersectionObserver {
  constructor(_callback, _options) {}
  observe() {}
  unobserve() {}
  disconnect() {}
};

HTMLCanvasElement.prototype.getContext = () => {
  return {
    fillRect: () => {},
    clearRect: () => {},
    getImageData: () => ({ data: [] }),
    putImageData: () => {},
    createImageData: () => [],
    setTransform: () => {},
    drawImage: () => {},
    save: () => {},
    fillText: () => {},
    restore: () => {},
    beginPath: () => {},
    moveTo: () => {},
    lineTo: () => {},
    closePath: () => {},
    stroke: () => {},
    translate: () => {},
    scale: () => {},
    rotate: () => {},
    arc: () => {},
    fill: () => {},
    measureText: () => ({ width: 0 }),
    transform: () => {},
    rect: () => {},
    clip: () => {},
  };
};
