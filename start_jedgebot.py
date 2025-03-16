import subprocess
import os
import sys
import threading
import signal
import socket
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

# Find npm path (use npm.cmd for Windows)
npm_path = "C:\\Program Files\\nodejs\\npm.cmd"  # Ensure correct path

# Store processes globally
backend_process = None
frontend_process = None

# Get the local machine's IP address for network-wide access
local_ip = socket.gethostbyname(socket.gethostname())

# Use VITE_API_URL from .env, fallback to local IP
VITE_API_URL = os.getenv("VITE_API_URL", f"http://{local_ip}:8000")

# Determine whether to use 127.0.0.1 or local IP
host_ip = "127.0.0.1" if "localhost" in VITE_API_URL else local_ip


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

# Start FastAPI backend using Poetry (Green color)
backend_process = subprocess.Popen(
    [
        "poetry",
        "run",
        "uvicorn",
        "backend.api.main:app",
        "--host",
        host_ip,  # Uses localhost or network IP
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

# Start Vite frontend using correct npm.cmd path (Cyan color)
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

# Create threads to stream logs in real-time with different colors
backend_thread = threading.Thread(
    target=stream_logs, args=(backend_process, "BACKEND", Fore.GREEN)
)
frontend_thread = threading.Thread(
    target=stream_logs, args=(frontend_process, "FRONTEND", Fore.CYAN)
)

# Start log streaming
backend_thread.start()
frontend_thread.start()

# Wait for both processes to complete
try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    signal_handler(None, None)

# Ensure all threads finish
backend_thread.join()
frontend_thread.join()
