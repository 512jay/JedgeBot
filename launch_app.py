# /launch_app.py
# Launches FastAPI backend, Vite frontend, and MailHog for dev with flexibility.

import subprocess
import os
import sys
import threading
import signal
import socket
import time
import psycopg2
import requests
import netifaces
import qrcode
import argparse
from urllib.parse import urlparse
from colorama import init, Fore
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
import os

# Parse command-line args
parser = argparse.ArgumentParser()
parser.add_argument(
    "--use-production-db",
    action="store_true",
    help="Use the production database (.env.production)",
)
args = parser.parse_args()
# --------------------- #
# 📁 Load Env File
# --------------------- #
env_filename = ".env.production" if args.use_production_db else ".env"
env_path = os.path.join("backend", env_filename)
loaded = load_dotenv(env_path, override=True)
print(f"✅ Loaded env file: {env_path} -> {loaded}")


project_root = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.join(project_root, "backend")



# ------------------------------------- #
# 📡 QR Code Utility
# ------------------------------------- #
def get_lan_ips():
    lan_ips = []
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        ipv4 = addrs.get(netifaces.AF_INET)
        if ipv4:
            for addr in ipv4:
                ip = addr.get("addr")
                if ip and not ip.startswith("127.") and not ip.startswith("169.254."):
                    lan_ips.append(ip)
    return lan_ips


# ------------------------------------- #
# 📍 Environment Setup
# ------------------------------------- #
init(autoreset=True)
project_root = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.join(project_root, "backend")
frontend_path = os.path.join(project_root, "frontend")
npm_path = os.getenv("NPM_PATH", "C:\\Program Files\\nodejs\\npm.cmd")

local_ip = socket.gethostbyname(socket.gethostname())
VITE_API_URL = os.getenv("VITE_API_URL", f"http://{local_ip}:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", f"http://localhost:5173")

from backend.core.settings import settings
DATABASE_URL = settings.DATABASE_URL
parsed_db = urlparse(os.getenv("DATABASE_URL", ""))
if not parsed_db.hostname:
    print(f"{Fore.RED}🚫 DATABASE_URL is not set or malformed!")
    sys.exit(1)

masked = f"{parsed_db.scheme}://{parsed_db.username}@***:{parsed_db.port}/{parsed_db.path.lstrip('/')}"
print(
    Fore.BLUE
    + f"📦 Connected to DB: {parsed_db.hostname} ({'RENDER' if parsed_db.hostname != 'localhost' else 'LOCAL'})"
)



# ------------------------------------- #
# 🐘 PostgreSQL Check (from DATABASE_URL)
# ------------------------------------- #
def wait_for_db():
    if not parsed_db.hostname:
        print(f"{Fore.RED}🚫 DATABASE_URL is empty or malformed.")
        sys.exit(1)

    max_retries = 10
    for i in range(max_retries):
        try:
            psycopg2.connect(
                dbname=parsed_db.path[1:],
                user=parsed_db.username,
                password=parsed_db.password,
                host=parsed_db.hostname,
                port=parsed_db.port or 5432,
                connect_timeout=3,
            ).close()
            print(f"{Fore.GREEN}✅ Database is ready!")
            return
        except psycopg2.OperationalError as e:
            print(f"{Fore.YELLOW}Waiting for DB... ({i + 1}/{max_retries})")
            time.sleep(5)
    print(f"{Fore.RED}❌ Could not connect to DB after {max_retries} retries.")
    sys.exit(1)


# ------------------------------------- #
# 🧾 Shared Logging Utility
# ------------------------------------- #
def stream_logs(process, prefix, color):
    try:
        for line in iter(process.stdout.readline, ""):
            output = line.strip()
            if isinstance(output, bytes):
                output = output.decode("utf-8", errors="ignore")
            print(f"{color}[{prefix}] {output}")
    except Exception as e:
        print(f"{color}[{prefix}] Log stream error: {e}")
    finally:
        process.stdout.close()


# ------------------------------------- #
# 🧼 Cleanup
# ------------------------------------- #
def terminate_processes():
    for proc, label in [
        (backend_process, "BACKEND"),
        (frontend_process, "FRONTEND"),
    ]:
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait()
            print(f"{Fore.YELLOW}[{label}] Terminated.")
    print(f"{Fore.YELLOW}Shutdown complete.")


def signal_handler(sig, frame):
    terminate_processes()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ------------------------------------- #
# 🚀 Startup
# ------------------------------------- #
wait_for_db()

backend_process = subprocess.Popen(
    [
        "poetry",
        "run",
        "uvicorn",
        "backend.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--reload",
    ],
    cwd=project_root,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)
threading.Thread(
    target=stream_logs, args=(backend_process, "BACKEND", Fore.GREEN)
).start()


def wait_for_backend(url=f"{VITE_API_URL}/auth/me", timeout=15):
    print(f"{Fore.YELLOW}⏳ Waiting for backend to start...")
    for i in range(timeout):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in [200, 401]:
                print(f"{Fore.GREEN}✅ Backend is ready!")
                return
        except Exception:
            pass
        print(f"{Fore.YELLOW}Retry {i + 1}/{timeout}...")
        time.sleep(1)
    print(f"{Fore.RED}❌ Backend failed to start.")
    sys.exit(1)


wait_for_backend()

frontend_process = subprocess.Popen(
    [npm_path, "run", "dev", "--", "--host", "0.0.0.0"],
    cwd=frontend_path,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)
threading.Thread(
    target=stream_logs, args=(frontend_process, "FRONTEND", Fore.CYAN)
).start()


try:
    frontend_process.wait()
    backend_process.wait()
except KeyboardInterrupt:
    signal_handler(None, None)
