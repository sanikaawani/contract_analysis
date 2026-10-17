"""
Unified launcher script for Legal Contract Risk Analysis System.
Starts the Flask Backend API and Vite Frontend Server.
"""
import subprocess
import sys
import os
import time

def start_backend():
    backend_script = os.path.join(os.path.dirname(__file__), "backend", "app.py")
    print("[*] Starting Flask Backend API on http://127.0.0.1:5000 ...")
    return subprocess.Popen([sys.executable, backend_script])

def start_frontend():
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    print("[*] Starting Vite React Frontend on http://localhost:5173 ...")
    # npm run dev on Windows
    npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
    return subprocess.Popen([npm_cmd, "run", "dev"], cwd=frontend_dir)

if __name__ == "__main__":
    print("=" * 70)
    print(" AI-Based Contract Risk Analysis and Clause Detection System")
    print(" Final Year NLP & Legal-Tech Project")
    print("=" * 70)
    
    b_proc = start_backend()
    time.sleep(2)
    f_proc = start_frontend()
    
    print("\n[+] Both servers are active!")
    print("    Backend API: http://127.0.0.1:5000")
    print("    Frontend UI: http://localhost:5173")
    print("    Press Ctrl+C to terminate both servers.\n")
    
    try:
        b_proc.wait()
        f_proc.wait()
    except KeyboardInterrupt:
        print("\n[*] Shutting down servers...")
        b_proc.terminate()
        f_proc.terminate()
        print("[+] Done.")
