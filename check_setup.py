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

print()
print("ALL GOOD" if failures == 0 else f"{failures} problem(s) to fix")
sys.exit(1 if failures else 0)