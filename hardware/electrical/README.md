# Electrical

Owner: electrical & hardware integration (1 member)

## What goes here
- Wiring diagram (PDF)
- ESP32 pin map (which pin drives what)
- Parts list (sensors, drivers, power supply)

ESP32 code lives in firmware/, not here.

## Boards in use

### ESP32 controller
| What | Value |
| --- | --- |
| Board | ESP32 ESP-32S 30-pin NodeMCU development board, probably a generic Chinese-made clone (the "ESP32 DevKit V1, 30-pin" line in the v2.5 BOM) |
| Bought from | RoboticsBD, product 948: https://store.roboticsbd.com/development-boards/948-esp32-esp-32s-30p-nodemcu-development-board-wireless-wifi-robotics-bangladesh.html |
| Module | ESP-32S, built around the original ESP32 chip (not ESP32-S2 or ESP32-S3) |
| Build target | Arduino IDE / arduino-cli: `esp32:esp32:esp32` ("ESP32 Dev Module"). pioarduino: `board = esp32dev` |
| Power | Laptop USB only (Rev D): nothing connects to VIN/5V |
| Pins used (Rev D) | 25 EN, 26 STEP, 27 DIR, 23 top light, 19 back light, 18 servo, 34 motion-power sense |
| Serial | 115200 baud; open with DTR/RTS off so the board doesn't reset |

Still to check on the real board:
- [ ] USB-to-serial chip (printed next to the USB socket: CP2102, CH340 or CH9102) and its USB ID (VID:PID). `link.py` finds the port by this ID.
- [ ] The metal can on the module reads ESP-32S (or ESP32-WROOM-32), so the chip is the original ESP32.
- [ ] Pins 18, 19, 23, 25, 26, 27 and 34 are all broken out on this board's headers (compare the silkscreen with the Rev D pin map).
- [ ] Windows shows a COM port when it's plugged in. Clones often use a CH340/CH9102 chip, which may need the WCH driver first.
- [ ] Upload works without touching the board. If it sticks at `Connecting...`, hold the BOOT button until writing starts (some clones' auto-reset is unreliable).
