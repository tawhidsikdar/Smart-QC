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
| USB-to-serial chip | WCH CH9102X |
| Serial | 115200 baud; open with DTR/RTS off so the board doesn't reset |

Still to check on the real board:
- [x] USB-to-serial chip: CH9102X.
- [ ] Its USB ID (VID:PID), read with the board plugged in (`arduino-cli board list` or Device Manager). Expect VID 1A86 (WCH); 55D4 is the usual CH9102 PID, but confirm it. `link.py` finds the port by this ID.
- [ ] The metal can on the module reads ESP-32S (or ESP32-WROOM-32), so the chip is the original ESP32.
- [ ] Pins 18, 19, 23, 25, 26, 27 and 34 are all broken out on this board's headers (compare the silkscreen with the Rev D pin map).
- [ ] Windows shows a COM port when it's plugged in. If it doesn't, install WCH's CH343/CH9102 driver (CH343SER) first.
- [ ] Upload works without touching the board. If it sticks at `Connecting...`, hold the BOOT button until writing starts (some clones' auto-reset is unreliable).
