# /scripts/validate_output.py
# Validates files staged in `chatgpt_output/` before merging into the main project.

import subprocess
import difflib
import os
from pathlib import Path
from shutil import copyfile

# Define paths
STAGING_DIR = Path("chatgpt_output")
TARGET_DIR = Path(".")


def run_black_check(filepath: Path) -> bool:
    result = subprocess.run(
        ["black", "--check", str(filepath)], capture_output=True, text=True
    )
    return result.returncode == 0


def run_mypy_check(filepath: Path) -> bool:
    if filepath.suffix == ".py":
        result = subprocess.run(["mypy", str(filepath)], capture_output=True, text=True)
        return result.returncode == 0
    return True


def display_diff(original: Path, new: Path):
    if not original.exists():
        print(f"[NEW FILE] {new.name}")
        return

    with open(original) as f1, open(new) as f2:
        diff = list(
            difflib.unified_diff(
                f1.readlines(),
                f2.readlines(),
                fromfile=str(original),
                tofile=str(new),
            )
        )

    if diff:
        print("".join(diff))
    else:
        print(f"[NO DIFF] {new.name}")


def validate_and_prompt():
    if not STAGING_DIR.exists():
        print("No staged files found.")
        return

    for file in STAGING_DIR.glob("*"):
        print(f"\n🔍 Validating: {file.name}")
        valid = run_black_check(file) and run_mypy_check(file)

        if not valid:
            print(f"❌ Lint/type check failed for {file.name}")
            continue

        # Determine target path
        rel_path = input(
            f"Where should {file.name} be saved to in the project? (relative path): "
        ).strip()
        target_path = TARGET_DIR / rel_path

        display_diff(target_path, file)

        confirm = (
            input(f"✅ Copy {file.name} to {target_path}? [y/N]: ").strip().lower()
        )
        if confirm == "y":
            target_path.parent.mkdir(parents=True, exist_ok=True)
            copyfile(file, target_path)
            print(f"✔️ Copied to {target_path}")
        else:
            print(f"Skipped {file.name}")


if __name__ == "__main__":
    validate_and_prompt()
