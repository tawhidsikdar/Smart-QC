# firmware - ESP32 code: motor, servo, chalk pen, safety stop

Board: ESP32 ESP-32S 30-pin NodeMCU (RoboticsBD). The chip is the original ESP32, not S2/S3.
Details and checks: `hardware/electrical/README.md`, "Boards in use".

| Tool | Board setting |
| --- | --- |
| pioarduino (main firmware build) | `board = esp32dev` in `platformio.ini` |
| Arduino IDE / arduino-cli (bench tests) | FQBN `esp32:esp32:esp32` ("ESP32 Dev Module") |

## Pinned versions (both tools must match)
| What | Version | Where it's set |
| --- | --- | --- |
| Arduino-ESP32 core | 3.3.13 | pioarduino `55.03.313` in `platformio.ini`; Arduino IDE Boards Manager "esp32 by Espressif Systems" 3.3.13 |
| FastAccelStepper | 2.0.1 | `lib_deps` in `platformio.ini`; Arduino IDE Library Manager 2.0.1 |

Don't click "Update" in the Arduino IDE for these two. Core 4.x is new (Nov 2026) and
FastAccelStepper isn't tested on it yet; move up only on purpose, after the gates.

## Build and upload (pioarduino)
Open **this `firmware` folder** in VS Code (File > Open Folder), not the whole repo: pioarduino
treats the folder that holds `platformio.ini` as the project. Code goes in `src/main.cpp`.

| Job | VS Code (blue bar at the bottom) | Command line, run inside `firmware/` |
| --- | --- | --- |
| Build | check mark | `pio run` |
| Upload | right arrow | `pio run -t upload` |
| Serial monitor | plug icon | `pio device monitor` |

- `pio` lives in `%USERPROFILE%\.platformio\penv\Scripts\`. The pioarduino terminal in VS Code already
  knows it; a normal terminal needs the full path.
- Uploading resets the ESP32 (that's normal). Opening the monitor does not, because
  `platformio.ini` turns DTR/RTS off.
- If an upload sits at `Connecting...`, hold the board's BOOT button until writing starts.
- The first build compiles the whole ESP32 core, so it takes a few minutes (on a new computer it
  also downloads the pinned tools first). Later builds take seconds.

## Pin map and one-step upload
- `include/pins.h` holds the Rev D pin map. Firmware uses these names only, never raw pin numbers.
  Change it only after a new revision of the Electrical Master Document.
- `tools/flash.py` finds the board by its USB chip ID (CH9102/CH343), uploads, then prints the first
  seconds of serial output without resetting the board. Close the serial monitor first. Run inside `firmware/`:
  `%USERPROFILE%\.platformio\penv\Scripts\python.exe tools\flash.py --expect alive`
