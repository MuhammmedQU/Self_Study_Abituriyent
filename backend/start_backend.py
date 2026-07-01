#!/usr/bin/env python3
"""Remove .venv and start backend server"""
import shutil
import os
import subprocess
import sys

print("Removing .venv directory...")
venv_path = ".venv"
if os.path.exists(venv_path):
    try:
        shutil.rmtree(venv_path)
        print(f"[OK] Removed {venv_path}")
    except Exception as e:
        print(f"[ERROR] Failed to remove {venv_path}: {e}")
else:
    print(f"[OK] {venv_path} does not exist")

print("\nStarting backend server on port 8000...")
print("=" * 60)

# Get the full python executable path
python_exe = sys.executable
print(f"Using Python: {python_exe}\n")

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
print(f"Working directory: {os.getcwd()}\n")

# Start the server - use the full path to be explicit
try:
    result = subprocess.run(
        [python_exe, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
        cwd=backend_dir
    )
    sys.exit(result.returncode)
except Exception as e:
    print(f"Error starting server: {e}")
    sys.exit(1)
