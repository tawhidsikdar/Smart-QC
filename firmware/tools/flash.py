r"""Build, upload and check SmartQC firmware in one step.

Run from the firmware folder:
    %USERPROFILE%\.platformio\penv\Scripts\python.exe tools\flash.py [--expect TEXT] [--listen SECONDS]

What it does:
1. Finds the ESP32 by its USB chip ID (WCH CH9102 or CH343), never by a fixed COM number.
2. Checks the port isn't held by another program (for example an open serial monitor).
3. Builds and uploads with pioarduino.
4. Listens on serial with DTR/RTS off (so opening the port doesn't reset the board) and prints what it hears.
   With --expect, exits 0 only if that text appears.
"""
import argparse, os, subprocess, sys, time
import serial
from serial.tools import list_ports

WCH_IDS = {(0x1A86, 0x55D4): "CH9102", (0x1A86, 0x55D3): "CH343"}
PIO = os.path.expanduser(r"~\.platformio\penv\Scripts\pio.exe")
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAUD = 115200  # matches monitor_speed in platformio.ini and the v2.5 protocol


def find_board():
    matches = [p for p in list_ports.comports() if (p.vid, p.pid) in WCH_IDS]
    if not matches:
        others = ", ".join(f"{p.device} ({p.hwid})" for p in list_ports.comports()) or "none"
        sys.exit(f"NO BOARD: no CH9102/CH343 found. Other serial ports: {others}. "
                 "Check the USB cable carries data.")
    if len(matches) > 1:
        sys.exit("MORE THAN ONE BOARD: " + ", ".join(p.device for p in matches) + ". Unplug the extra one.")
    return matches[0]


def port_is_free(device):
    try:
        s = serial.Serial()
        s.port = device
        s.dtr = False; s.rts = False  # don't reset the board just to test the port
        s.open(); s.close()
        return True
    except serial.SerialException:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", help="text that must appear on serial after upload")
    ap.add_argument("--listen", type=float, default=6.0, help="seconds to listen after upload")
    args = ap.parse_args()

    board = find_board()
    print(f"Board: {WCH_IDS[(board.vid, board.pid)]} on {board.device} ({board.hwid})", flush=True)
    if not port_is_free(board.device):
        sys.exit(f"PORT BUSY: {board.device} is open in another program. Close the serial monitor and retry.")

    r = subprocess.run([PIO, "run", "-t", "upload", "--upload-port", board.device], cwd=PROJECT,
                       capture_output=True, text=True, errors="replace")
    out = (r.stdout + r.stderr).splitlines()
    print("\n".join(out[-25:]), flush=True)
    if r.returncode != 0:
        if any("Connecting" in l for l in out):
            print("HINT: if it stuck at 'Connecting...', hold the BOOT button during the next upload.")
        sys.exit("UPLOAD FAILED")

    s = serial.Serial()
    s.port, s.baudrate, s.timeout = board.device, BAUD, 0.5
    s.dtr = False; s.rts = False
    s.open()
    lines, end = [], time.time() + args.listen
    while time.time() < end:
        line = s.readline().decode(errors="replace").rstrip()
        if line:
            lines.append(line)
    s.close()
    print(f"--- Serial output ({args.listen:.0f} s):")
    print("\n".join(lines) or "(nothing received)")
    if args.expect and not any(args.expect in l for l in lines):
        sys.exit(f"CHECK FAILED: '{args.expect}' not seen on serial")
    print("OK")


if __name__ == "__main__":
    main()
