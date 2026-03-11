
"""
Quick start script to run the Dog API Service with a mock backend.
This starts both the mock dog service and the main API for testing in Swagger UI.
"""
import subprocess
import time
import os
import sys
from dotenv import load_dotenv

# Change to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print("=" * 70)
print("Dog API Service - Quick Start with Swagger Testing")
print("=" * 70)
print(f"Working directory: {os.getcwd()}")
print()

# Check if .env exists and create it FIRST before any imports
if not os.path.exists(".env"):
    print("Creating .env file...")
    with open(".env", "w") as f:
        f.write("PET_SERVICE_BASE_URL=http://localhost:8001\n")
        f.write("DOGAPI_BASE_URL=http://localhost:8001\n")
    print(".env created successfully")
else:
    print(".env file already exists")

print()

# Load environment variables from .env
load_dotenv()
print("Environment variables loaded from .env")
print()
print("[1/2] Starting mock Dog API service on http://localhost:8001")
mock_proc = subprocess.Popen(
    ["python", "mock_service.py"],
    cwd=script_dir
)
time.sleep(2)  # Give mock service time to start

# Start main API
print("[2/2] Starting Dog API Service on http://localhost:8000")
print()
print("=" * 70)
print("🚀 Services are running!")
print()
print("📋 API Documentation (Swagger UI):")
print("   http://localhost:8000/docs")
print()
print("📖 Alternative API Documentation (ReDoc):")
print("   http://localhost:8000/redoc")
print()
print("🔧 Mock Dog API Service (for testing):")
print("   http://localhost:8001")
print()
print("💡 Available endpoints to test:")
print("   • GET  /breeds - List all dog breeds")
print("   • GET  /breeds/{id} - Get specific breed by ID")
print("   • GET  /facts - Get random dog facts")
print("   • GET  /groups - List dog breed groups")
print("   • GET  /groups/{id} - Get specific group by ID")
print("   • POST /pets - Create a pet (legacy endpoint)")
print()
print("Press Ctrl+C to stop all services")
print("=" * 70)
print()

try:
    subprocess.run(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"], cwd=script_dir)
except KeyboardInterrupt:
    print("\n\nShutting down...")
    mock_proc.terminate()
    mock_proc.wait()
    print("Services stopped.")
except Exception as e:
    print(f"Error starting uvicorn: {e}")
    print(f"Make sure you're in the correct directory: {script_dir}")
    mock_proc.terminate()
    mock_proc.wait()
