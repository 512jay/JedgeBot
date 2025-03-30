// /scripts/add-or-correct-path-comments.js
// Ensures each file starts with a correct file location comment

const fs = require("fs");
const path = require("path");

const SRC_DIR = path.join(__dirname, "..", "frontend", "src");
const supportedExtensions = [".js", ".jsx", ".ts", ".tsx"];

function getAllCodeFiles(dir) {
  const files = [];
  for (const item of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      files.push(...getAllCodeFiles(fullPath));
    } else if (supportedExtensions.includes(path.extname(fullPath))) {
      files.push(fullPath);
    }
  }
  return files;
}

function isPathComment(line) {
  return /^\/\/\s*\/frontend\/src\/.+\.(js|jsx|ts|tsx)$/.test(line.trim());
}

function normalizePath(filePath) {
  const relPath = filePath.split("frontend")[1].replace(/\\/g, "/");
  return `// /frontend${relPath}`;
}

function updateFile(filePath) {
  const expectedComment = normalizePath(filePath);
  const originalContent = fs.readFileSync(filePath, "utf-8");
  const lines = originalContent.split("\n");

  let updated = false;
  let insertAtTop = true;

  // Remove all path-style comments in first 5 lines
  const cleanedLines = lines.filter((line, index) => {
    if (index < 5 && isPathComment(line)) {
      updated = true;
      return false; // remove
    }
    return true;
  });

  // Check if the first line was a path comment
  if (isPathComment(lines[0])) {
    // Replace with correct comment if needed
    cleanedLines.unshift(expectedComment);
    updated = true;
    insertAtTop = false;
  }

  if (insertAtTop) {
    cleanedLines.unshift(expectedComment);
    updated = true;
  }

  if (updated) {
    fs.copyFileSync(filePath, filePath + ".bak");
    fs.writeFileSync(filePath, cleanedLines.join("\n"), "utf-8");
    console.log(`📎 Updated: ${filePath.replace(/\\/g, "/")}`);
  }
}

function main() {
  console.log("🔍 Checking and updating file location headers...");
  const files = getAllCodeFiles(SRC_DIR);
  files.forEach(updateFile);
  console.log("✅ Done! .bak backups created.");
}

main();
