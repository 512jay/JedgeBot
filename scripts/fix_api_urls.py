# /scripts/fix_api_urls.py
# Script to patch frontend files to use `API_URL` for fetch calls

import os
import re

FRONTEND_DIR = "frontend/src"
ENV_LINE = "const API_URL = import.meta.env.VITE_API_URL;"


def should_patch_file(filepath: str) -> bool:
    return filepath.endswith((".js", ".jsx", ".ts", ".tsx")) and not any(
        x in filepath for x in [".bak", "__tests__"]
    )


def patch_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(
        "import.meta.env.VITE_API_URL" in line or "API_URL" in line for line in lines
    ):
        already_has_api_url = True
    else:
        already_has_api_url = False

    modified = False
    new_lines = []
    inserted_env_line = False

    for line in lines:
        if re.search(r'fetch\((["\'])\/', line):
            line = re.sub(
                r'fetch\((["\'])(\/[^\'"]+)(["\'])', r"fetch(`${API_URL}\2`)", line
            )
            modified = True

        new_lines.append(line)

    if modified and not already_has_api_url:
        # Insert ENV_LINE after the last import or at the top
        for i, line in enumerate(new_lines):
            if not inserted_env_line and re.match(r"^\s*import ", line):
                continue
            new_lines.insert(i, ENV_LINE + "\n")
            inserted_env_line = True
            break
        if not inserted_env_line:
            new_lines.insert(0, ENV_LINE + "\n")

    if modified or not already_has_api_url:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ Patched: {filepath}")
    else:
        print(f"✅ Skipped (no changes needed): {filepath}")


def main():
    for root, _, files in os.walk(FRONTEND_DIR):
        for file in files:
            path = os.path.join(root, file)
            if should_patch_file(path):
                patch_file(path)


if __name__ == "__main__":
    main()
