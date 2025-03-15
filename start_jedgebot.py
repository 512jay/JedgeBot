import subprocess
import os
import sys
import threading
from colorama import init, Fore

# Initialize colorama for Windows terminal compatibility
init(autoreset=True)

# Define absolute paths
project_root = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.join(project_root, "backend")
frontend_path = os.path.join(project_root, "frontend")

# Find npm path (use npm.cmd for Windows)
npm_path = "C:\\Program Files\\nodejs\\npm.cmd"  # Ensure correct path


# Function to continuously read and print process logs with colors
def stream_logs(process, prefix, color):
    for line in iter(process.stdout.readline, ""):
        print(f"{color}[{prefix}] {line.strip()}")
    process.stdout.close()


# Start FastAPI backend using Poetry (Green color)
backend_process = subprocess.Popen(
    [
        "poetry",
        "run",
        "uvicorn",
        "backend.api.main:app",
        "--host",
        "0.0.0.0",
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
    [npm_path, "run", "dev"],
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
backend_process.wait()
frontend_process.wait()

# Ensure all threads finish
backend_thread.join()
frontend_thread.join()
