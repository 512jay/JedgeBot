// /scripts/convert-public-image-refs.js
// Script to convert "/images/..." src URLs to imports from "@/images/..."
// Run with: node scripts/convert-public-image-refs.js

const fs = require("fs");
const path = require("path");

const SRC_DIR = path.join(__dirname, "..", "frontend", "src");

const IMG_REGEX = /["']\/images\/([^"']+\.(png|jpe?g|webp|svg|gif))["']/g;
const IMG_TAG_REGEX = /<img\s+[^>]*src=["']\/images\/([^"']+)["'][^>]*>/gi;

function getAllJSFiles(dir) {
  const files = [];
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      files.push(...getAllJSFiles(fullPath));
    } else if (fullPath.endsWith(".jsx") || fullPath.endsWith(".js")) {
      files.push(fullPath);
    }
  }
  return files;
}

function createImportName(imagePath) {
  const baseName = path.basename(imagePath).split(".")[0];
  return baseName.replace(/[^a-zA-Z0-9]/g, "") + "Image";
}

function processFile(filePath) {
  let content = fs.readFileSync(filePath, "utf-8");
  let updated = false;
  const importMap = new Map();

  // Find all /images/... paths
  const matches = [...content.matchAll(IMG_REGEX)];

  if (matches.length === 0) return;

  matches.forEach((match) => {
    const fullMatch = match[0]; // "/images/hero/foo.webp"
    const imgPath = match[1]; // "hero/foo.webp"

    const importVar = createImportName(imgPath);
    importMap.set(imgPath, importVar);

    // Replace image string with import variable
    const importRegex = new RegExp(`["']/images/${imgPath}["']`, "g");
    content = content.replace(importRegex, importVar);
    updated = true;
  });

  // Add import statements
  if (importMap.size > 0) {
    const importLines = Array.from(importMap.entries()).map(
      ([imgPath, importVar]) =>
        `import ${importVar} from "@/images/${imgPath}";`
    );
    const firstImportIndex = content.indexOf("import");

    // Insert imports before the first import statement
    content =
      importLines.join("\n") + "\n" + content;
  }

  if (updated) {
    fs.copyFileSync(filePath, filePath + ".bak"); // backup
    fs.writeFileSync(filePath, content, "utf-8");
    console.log(`✅ Updated: ${filePath}`);
  }
}

function main() {
  console.log("🔍 Scanning for hardcoded /images/... references...");
  const files = getAllJSFiles(SRC_DIR);
  files.forEach(processFile);
  console.log("🎉 Done. Backup copies saved with .bak extension.");
}

main();
