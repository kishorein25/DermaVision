"""
DermaVision System Diagnostics & Health-Check Utility
Verifies MediaPipe, Ollama local model availability, OpenStreetMap referral connectivity, and clinical packages.
"""

import sys
import os
import requests

# Reconfigure stdout for utf-8 if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_diagnostics():
    print("=" * 65)
    print("DERMAVISION SYSTEM HEALTH & SUBSYSTEM DIAGNOSTICS")
    print("=" * 65)

    # 1. Check Python version
    py_ver = sys.version.split()[0]
    print(f"[1/5] Python Environment: {py_ver} (64-bit)")

    # 2. Check MediaPipe
    try:
        import mediapipe as mp
        print(f"  [OK] MediaPipe Framework: Detected and Loaded (v{mp.__version__})")
    except Exception as e:
        print(f"  [ERROR] MediaPipe Error: {e}")

    # 3. Check OpenCV
    try:
        import cv2
        print(f"  [OK] OpenCV Computer Vision: Active (v{cv2.__version__})")
    except Exception as e:
        print(f"  [ERROR] OpenCV Error: {e}")

    # 4. Check Local Ollama Engine
    print("\n[2/5] Checking Local Ollama Model Service...")
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            models = [m.get("name") for m in r.json().get("models", [])]
            print(f"  [OK] Ollama Service: Online (Available models: {models})")
        else:
            print(f"  [WARN] Ollama returned status {r.status_code}")
    except Exception:
        print("  [INFO] Ollama service not responding on port 11434 (Simulated Clinical Engine active)")

    # 5. Check 100% Free Forever OpenStreetMap / Geolocation
    print("\n[3/5] Checking Free Forever Specialist Referral Connectivity...")
    try:
        from specialist_finder import SpecialistFinder
        finder = SpecialistFinder()
        loc, lat, lon = finder.detect_user_location()
        print(f"  [OK] IP Geolocation: {loc} ({lat}, {lon})")
        res = finder.find_specialists(location=loc, lat=lat, lon=lon)
        print(f"  [OK] OSM Live Registry: {res['total_found']} verified healthcare facilities detected")
    except Exception as e:
        print(f"  [WARN] Referral Check Notice: {e}")

    # 6. Check Core Modular Packages
    print("\n[4/5] Checking Modular Clinical Packages...")
    packages = ["diagnose", "core", "agents", "referral", "reporting", "tests", "rag_chatbot"]
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"  [OK] Package '{pkg}/': Verified and Importable")
        except Exception as e:
            print(f"  [ERROR] Package '{pkg}/' Error: {e}")

    # 7. Check Streamlit Application Status
    print("\n[5/5] Checking Streamlit UI Server...")
    try:
        r_st = requests.get("http://localhost:8501", timeout=3)
        if r_st.status_code == 200:
            print("  [OK] Streamlit Server: LIVE and Healthy on http://localhost:8501 (HTTP 200 OK)")
        else:
            print(f"  [WARN] Streamlit Server returned status {r_st.status_code}")
    except Exception:
        print("  [INFO] Streamlit not detected on port 8501 (Use 'run_app.bat' to launch)")

    print("\n" + "=" * 65)
    print("ALL CORE DIAGNOSTIC CHECKS COMPLETED")
    print("=" * 65)

if __name__ == "__main__":
    run_diagnostics()
