import subprocess
import os

# Define absolute paths
project_root = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.join(project_root, "backend")
frontend_path = os.path.join(project_root, "frontend")

# Start FastAPI backend
backend_process = subprocess.Popen(
    ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
    cwd=backend_path,
    shell=True,
)

# Start Vite frontend
frontend_process = subprocess.Popen(
    ["npm", "run", "dev"], cwd=frontend_path, shell=True
)

# Wait for both processes
backend_process.wait()
frontend_process.wait()
