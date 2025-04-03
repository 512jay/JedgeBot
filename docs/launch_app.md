# /launch_app.py
# Launches FastAPI backend and Vite frontend in development mode with proper readiness checks.

import subprocess
import os
import sys
import threading
import signal
import socket
import time
import psycopg2
import requests
from colorama import init, Fore
from dotenv import load_dotenv

# Initialize colorama for Windows terminal compatibility
init(autoreset=True)

# Load environment variables from .env
load_dotenv()

# Define absolute paths
project_root = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.join(project_root, "backend")
frontend_path = os.path.join(project_root, "frontend")

# Get npm path for Windows
npm_path = os.getenv("NPM_PATH", "C:\\Program Files\\nodejs\\npm.cmd")

# Get the local machine's IP address for network-wide access
local_ip = socket.gethostbyname(socket.gethostname())

# Get frontend and backend URLs from environment
VITE_API_URL = os.getenv("VITE_API_URL", f"http://{local_ip}:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", f"http://localhost:5173")

host_ip = "localhost" if "localhost" in VITE_API_URL else local_ip

# Store processes globally
backend_process = None
frontend_process = None


def wait_for_db():
    """Wait for PostgreSQL in Docker to be ready before starting FastAPI."""
    max_retries = 10
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                connect_timeout=3,
            )
            conn.close()
            print(f"{Fore.GREEN}Database is ready!")
            return
        except psycopg2.OperationalError:
            print(f"{Fore.YELLOW}Database not ready, retrying ({i+1}/{max_retries})...")
            time.sleep(5)

    print(f"{Fore.RED}Database connection failed after {max_retries} retries. Exiting.")
    sys.exit(1)


def wait_for_backend(url=f"{VITE_API_URL}/auth/me", timeout=15):
    """Wait for FastAPI backend to respond to HTTP requests before starting frontend."""
    print(f"{Fore.YELLOW}Waiting for backend to be fully ready...")
    for i in range(timeout):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in [200, 401]:
                print(f"{Fore.GREEN}Backend is ready! ✅")
                return
        except Exception:
            pass
        print(f"{Fore.YELLOW}Backend not ready yet... ({i+1}/{timeout})")
        time.sleep(1)

    print(f"{Fore.RED}Backend failed to start after {timeout} seconds.")
    sys.exit(1)


def stream_logs(process, prefix, color):
    """Function to continuously read and print process logs with colors."""
    try:
        for line in iter(process.stdout.readline, ""):
            print(f"{color}[{prefix}] {line.strip()}")
    except Exception as e:
        print(f"{color}[{prefix}] Log streaming error: {e}")
    finally:
        process.stdout.close()


def terminate_processes():
    """Gracefully terminate backend and frontend processes."""
    global backend_process, frontend_process

    print(f"{Fore.YELLOW}Shutting down processes...")

    if backend_process and backend_process.poll() is None:
        backend_process.terminate()
        backend_process.wait()
        print(f"{Fore.GREEN}[BACKEND] Process terminated.")

    if frontend_process and frontend_process.poll() is None:
        frontend_process.terminate()
        frontend_process.wait()
        print(f"{Fore.CYAN}[FRONTEND] Process terminated.")

    print(f"{Fore.YELLOW}Shutdown complete.")


def signal_handler(sig, frame):
    """Handle termination signals like Ctrl+C."""
    terminate_processes()
    sys.exit(0)


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Wait for PostgreSQL before starting FastAPI
wait_for_db()

# Start FastAPI backend using Poetry (Green color)
backend_process = subprocess.Popen(
    [
        "poetry",
        "run",
        "uvicorn",
        "backend.main:app",
        "--host",
        host_ip,
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

# Create thread to stream backend logs
backend_thread = threading.Thread(
    target=stream_logs, args=(backend_process, "BACKEND", Fore.GREEN)
)
backend_thread.start()

# Wait until backend is responding before launching frontend
wait_for_backend()

# Start Vite frontend (Cyan color)
frontend_process = subprocess.Popen(
    [
        npm_path,
        "run",
        "dev",
        "--",
        "--host",
        "localhost" if "localhost" in VITE_API_URL else local_ip,
    ],
    cwd=frontend_path,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

# Create thread to stream frontend logs
frontend_thread = threading.Thread(
    target=stream_logs, args=(frontend_process, "FRONTEND", Fore.CYAN)
)
frontend_thread.start()

# Wait for both to exit
try:
    frontend_process.wait()
    backend_process.wait()
except KeyboardInterrupt:
    signal_handler(None, None)

backend_thread.join()
frontend_thread.join()
