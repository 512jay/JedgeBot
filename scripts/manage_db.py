# /scripts/manage_db.py
# CLI for managing Alembic migrations with remote/local DB options.

import argparse
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv


def load_env(use_remote: bool) -> None:
    backend_path = Path(__file__).parent.parent / "backend"
    env_file = ".env.production" if use_remote else ".env"
    dotenv_path = backend_path / env_file
    loaded = load_dotenv(dotenv_path)
    print(
        f"✅ Loaded {'production' if use_remote else 'local'} env: {dotenv_path} -> {loaded}"
    )
    os.environ["DOTENV_FILE"] = str(dotenv_path)  # Used by Alembic helpers if needed


def run_alembic_command(command_args: list[str]) -> None:
    cmd_str = " ".join(command_args)
    print(f"🚀 Running: alembic {cmd_str}")
    try:
        subprocess.run(["alembic"] + command_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Alembic command failed: {e}")
        exit(e.returncode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Alembic DB migrations.")
    parser.add_argument(
        "--remote",
        action="store_true",
        help="Use remote .env.production database instead of local .env",
    )

    parser.add_argument(
        "alembic_args",
        nargs=argparse.REMAINDER,
        help=(
            "Alembic arguments, e.g.:\n"
            "  upgrade head\n"
            "  downgrade -1\n"
            "  revision -m 'add new table'\n"
            "  stamp head"
        ),
    )

    args = parser.parse_args()

    if not args.alembic_args:
        parser.print_help()
        print(
            "\n❌ You must provide Alembic arguments, like `upgrade head` or `revision -m 'msg'`"
        )
        exit(1)

    load_env(use_remote=args.remote)
    run_alembic_command(args.alembic_args)
