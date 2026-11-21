# firmware - ESP32 code: motor, servo, chalk pen, safety stop

Board: ESP32 ESP-32S 30-pin NodeMCU (RoboticsBD). The chip is the original ESP32, not S2/S3.
Details and checks: `hardware/electrical/README.md`, "Boards in use".

| Tool | Board setting |
| --- | --- |
| pioarduino (main firmware build) | `board = esp32dev` in `platformio.ini` |
| Arduino IDE / arduino-cli (bench tests) | FQBN `esp32:esp32:esp32` ("ESP32 Dev Module") |

Use the same Arduino-ESP32 core version in both tools.
