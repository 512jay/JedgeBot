// /frontend/alias.config.js
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export const alias = {
  '@/': resolve(__dirname, './src') + '/',
  '@feat': resolve(__dirname, './src/features'),
  '@auth': resolve(__dirname, './src/features/auth'),
  '@images': resolve(__dirname, './src/images'),
  '@styles': resolve(__dirname, './src/styles'),
  '@pages': resolve(__dirname, './src/pages'),
  '@useAuth': resolve(__dirname, './src/context/useAuth'),
  '@hooks': resolve(__dirname, './src/hooks'),
};
