# /launch_app.py
# Launches FastAPI backend, Vite frontend, and MailHog for dev with proper readiness checks.

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
from colorama import init, Fore
from dotenv import load_dotenv

# ----------------------------------------------------------------------------- #
# 📡 QR Code & IP Utility
# ----------------------------------------------------------------------------- #


def get_lan_ips():
    """Return a list of LAN-facing IPv4 addresses on active interfaces."""
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


def print_qr_in_terminal(data: str):
    """Render a compact QR code in the terminal."""
    qr_code = qrcode.QRCode(
        version=2,  # Lower number = smaller grid (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,  # Minimum white border
    )
    qr_code.add_data(data)
    qr_code.make(fit=True)
    qr_matrix = qr_code.get_matrix()

    for row in qr_matrix:
        print("".join("██" if cell else "  " for cell in row))


def show_qr_codes_for_lan(port: str = "5173"):
    """Detect all LAN IPs and print QR codes to access the frontend."""
    lan_ips = get_lan_ips()
    if not lan_ips:
        print(f"{Fore.RED}No LAN IPs found.")
        return
    print(f"{Fore.CYAN}🌐 Access your app from any of these on your network:")
    for ip in lan_ips:
        url = f"http://{ip}:{port}"
        print(f"{Fore.GREEN}→ {url}")
        print(f"{Fore.MAGENTA}📱 QR code for {ip}:")
        print_qr_in_terminal(url)
        print()


# ----------------------------------------------------------------------------- #
# 🔧 Setup & Config
# ----------------------------------------------------------------------------- #

init(autoreset=True)
load_dotenv()

project_root = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.join(project_root, "backend")
frontend_path = os.path.join(project_root, "frontend")

npm_path = os.getenv("NPM_PATH", "C:\\Program Files\\nodejs\\npm.cmd")

local_ip = socket.gethostbyname(socket.gethostname())
VITE_API_URL = os.getenv("VITE_API_URL", f"http://{local_ip}:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", f"http://localhost:5173")

backend_process = None
frontend_process = None
mailhog_process = None

# ----------------------------------------------------------------------------- #
# 🐷 MailHog Setup
# ----------------------------------------------------------------------------- #


def start_mailhog():
    global mailhog_process
    try:
        mailhog_process = subprocess.Popen(
            [
                "docker",
                "run",
                "--rm",
                "-p",
                "1025:1025",
                "-p",
                "8025:8025",
                "mailhog/mailhog",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        threading.Thread(
            target=stream_logs,
            args=(mailhog_process, "MAILHOG", Fore.MAGENTA),
            daemon=True,
        ).start()
        print(f"{Fore.MAGENTA}MailHog started: http://localhost:8025")
    except Exception as e:
        print(f"{Fore.RED}Failed to start MailHog: {e}")


# ----------------------------------------------------------------------------- #
# 🐘 PostgreSQL Waiter
# ----------------------------------------------------------------------------- #


def wait_for_db():
    max_retries = 10
    for i in range(max_retries):
        try:
            psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                connect_timeout=3,
            ).close()
            print(f"{Fore.GREEN}✅ Database is ready!")
            return
        except psycopg2.OperationalError:
            print(f"{Fore.YELLOW}Waiting for DB... ({i + 1}/{max_retries})")
            time.sleep(5)
    print(f"{Fore.RED}❌ DB connection failed after {max_retries} retries.")
    sys.exit(1)


# ----------------------------------------------------------------------------- #
# 🚦 Backend Readiness Check
# ----------------------------------------------------------------------------- #


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


# ----------------------------------------------------------------------------- #
# 🧾 Logging Utility
# ----------------------------------------------------------------------------- #


def stream_logs(process, prefix, color):
    try:
        for line in iter(process.stdout.readline, ""):
            print(f"{color}[{prefix}] {line.strip()}")
    except Exception as e:
        print(f"{color}[{prefix}] Log stream error: {e}")
    finally:
        process.stdout.close()


# ----------------------------------------------------------------------------- #
# 🔚 Graceful Shutdown
# ----------------------------------------------------------------------------- #


def terminate_processes():
    global backend_process, frontend_process
    print(f"{Fore.YELLOW}Shutting down processes...")
    if mailhog_process and mailhog_process.poll() is None:
        mailhog_process.terminate()
        mailhog_process.wait()
        print(f"{Fore.MAGENTA}[MAILHOG] Terminated.")
    if backend_process and backend_process.poll() is None:
        backend_process.terminate()
        backend_process.wait()
        print(f"{Fore.GREEN}[BACKEND] Terminated.")
    if frontend_process and frontend_process.poll() is None:
        frontend_process.terminate()
        frontend_process.wait()
        print(f"{Fore.CYAN}[FRONTEND] Terminated.")
    print(f"{Fore.YELLOW}Shutdown complete.")


def signal_handler(sig, frame):
    terminate_processes()
    sys.exit(0)


# ----------------------------------------------------------------------------- #
# 🚀 Launch All Systems
# ----------------------------------------------------------------------------- #

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

wait_for_db()
start_mailhog()

# ✅ Launch backend
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

wait_for_backend()

# ✅ Launch frontend
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

# ✅ Show QR codes for all LAN IPs
show_qr_codes_for_lan()

try:
    frontend_process.wait()
    backend_process.wait()
except KeyboardInterrupt:
    signal_handler(None, None)
