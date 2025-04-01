// /scripts/scanForHardcodedApi.mjs
// ES Module version of the scan script

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Emulate __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TARGET = 'http://localhost:8000';
const CONTEXT_SNIPPET = 'import.meta.env.VITE_API_URL || "http://localhost:8000"';
const EXTENSIONS = ['.js', '.jsx'];

const matchesWithoutEnvWrapper = (content) => {
  const lines = content.split('\n');
  return lines
    .map((line, index) => {
      if (line.includes(TARGET) && !line.includes('import.meta.env.VITE_API_URL')) {
        return { line: line.trim(), lineNumber: index + 1 };
      }
      return null;
    })
    .filter(Boolean);
};

const scanDir = (dir) => {
  fs.readdirSync(dir).forEach((file) => {
    const filepath = path.join(dir, file);
    const stat = fs.statSync(filepath);

    if (stat.isDirectory()) {
      scanDir(filepath);
    } else if (
      EXTENSIONS.includes(path.extname(file)) &&
      !file.endsWith('.bak')
    ) {
      const content = fs.readFileSync(filepath, 'utf8');
      const matches = matchesWithoutEnvWrapper(content);

      if (matches.length > 0) {
        console.log(`\n🔍 Found in: ${filepath}`);
        matches.forEach(({ line, lineNumber }) => {
          console.log(`  ${lineNumber}: ${line}`);
        });
      }
    }
  });
};

console.log("🚨 Scanning for hardcoded 'http://localhost:8000' that are not using VITE_API_URL...");
scanDir(path.join(__dirname, '..', 'src'));
console.log('\n✅ Scan complete. No replacements were made.');
