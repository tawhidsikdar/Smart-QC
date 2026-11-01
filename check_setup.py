"""SmartQC setup check.
Run from the repo folder:  python check_setup.py
OK = good, WARN = not ready yet (fine before hardware arrives), FAIL = must fix.
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # the repo folder, wherever it is on this computer
failures = 0


def report(status, name, detail=""):
    """Print one result line and count failures."""
    global failures
    if status == "FAIL":
        failures += 1
    print(f"[{status:<4}] {name:<12} {detail}")


# 1. Python version
v = sys.version_info
if (v.major, v.minor) == (3, 11):
    report("OK", "Python", f"{v.major}.{v.minor}.{v.micro}")
else:
    report("FAIL", "Python", f"{v.major}.{v.minor} found, need 3.11")

# 2. Packages (import names, not install names)
for name in ["numpy", "cv2", "serial", "yaml", "streamlit", "pandas", "torch", "ultralytics"]:
    try:
        module = importlib.import_module(name)
        report("OK", name, getattr(module, "__version__", ""))
    except ImportError:
        report("FAIL", name, "not installed in this environment")

if failures:
    print("\nFix the packages above first, then run again.")
    sys.exit(1)

# 3. Config file
config_path = ROOT / "config.local.yaml"
if not config_path.exists():
    report("FAIL", "Config", "config.local.yaml missing: copy config.example.yaml and edit it")
    sys.exit(1)

import yaml
with open(config_path, encoding="utf-8") as f:
    config = yaml.safe_load(f)
report("OK", "Config", config_path.name)

# 4. GPU or CPU
import torch
device = str(config["model"]["device"])
if device == "cpu":
    report("OK", "Compute", "CPU (set in config)")
elif torch.cuda.is_available():
    report("OK", "Compute", f"GPU {torch.cuda.get_device_name(0)}")
else:
    report("FAIL", "Compute", "config asks for GPU but CUDA is not available")
# 5. Camera (WARN only: the C920 may not be plugged in yet)
import cv2
cam_index = config["camera"]["index"]
cap = cv2.VideoCapture(cam_index)
ok = False
if cap.isOpened():
    ok, frame = cap.read()
cap.release()
if ok:
    height, width = frame.shape[:2]
    report("OK", "Camera", f"index {cam_index}, {width}x{height}")
else:
    report("WARN", "Camera", f"no picture from camera index {cam_index}")

# 6. ESP32 serial port (WARN only: the board may not be plugged in)
from serial.tools import list_ports
port = str(config["esp32"]["port"])
ports_seen = [p.device for p in list_ports.comports()]
if port in ports_seen:
    report("OK", "ESP32 port", port)
else:
    report("WARN", "ESP32 port", f"{port} not found; ports seen: {ports_seen or 'none'}")

# 7. Trained model file (WARN only: there is no model before training)
model_path = ROOT / config["model"]["path"]
if model_path.exists():
    report("OK", "Model", model_path.name)
else:
    report("WARN", "Model", f"{config['model']['path']} not found (normal before training)")

print()
print("ALL GOOD" if failures == 0 else f"{failures} problem(s) to fix")
sys.exit(1 if failures else 0)