// SmartQC firmware - starter sketch.
// Checks the toolchain and upload path only: blinks the onboard LED and prints over serial.
// It does not touch any Rev D pins (18, 19, 23, 25, 26, 27, 34), so nothing on the rig moves.

#include <Arduino.h>
#include "pins.h"

void setup() {
  Serial.begin(115200);     // matches monitor_speed in platformio.ini
  pinMode(PIN_BOARD_LED, OUTPUT);
  Serial.println();
  Serial.println("SmartQC starter sketch running");
}

void loop() {
  static uint32_t count = 0;
  digitalWrite(PIN_BOARD_LED, HIGH);
  delay(500);
  digitalWrite(PIN_BOARD_LED, LOW);
  delay(500);
  Serial.printf("alive %lu\n", static_cast<unsigned long>(++count));
}
