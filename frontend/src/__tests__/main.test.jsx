// frontend/src/__tests__/main.test.jsx
import { expect, it } from 'vitest';
import '@/main'; // This is enough to load the app and ensure no crashes

it('renders without crashing', () => {
  expect(true).toBe(true); // Just confirms loading the file doesn't throw
});
