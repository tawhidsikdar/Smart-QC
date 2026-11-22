#pragma once
#include <Arduino.h>
// SmartQC carrier board Rev E (pin map unchanged from Rev D): the only ESP32 pins firmware may use.
// Source of truth: Electrical Master Document Rev D "Settings and pin map", plus the Rev E change document
// (hardware/electrical/), which confirms: "Pins stay as Rev D".
// Change this file only after a new hardware revision of the master document.
// All other GPIOs are unconnected on the board. Strapping pins (0, 2, 5, 12, 15) and USB serial (1, 3) are avoided.

constexpr uint8_t PIN_EN    = 25; // T9 EN    -> TMC2209 EN. LOW = driver on. R1 10k pulls HIGH (off) at reset.
constexpr uint8_t PIN_STEP  = 26; // T9 STEP  -> TMC2209 STEP. One rising edge = one 1/8 microstep.
constexpr uint8_t PIN_DIR   = 27; // T10 DIR  -> TMC2209 DIR. Forward level: found on the bench (not known yet).
constexpr uint8_t PIN_TOP   = 23; // T10 TOP  -> R10 -> U5 pin 9/8 -> R2 -> Q1 gate. HIGH = top light on. 25 kHz PWM.
constexpr uint8_t PIN_BACK  = 19; // T13 BACK -> R11 -> U5 pin 12/11 -> R13 -> Q2 gate. HIGH = back light on. 25 kHz PWM.
constexpr uint8_t PIN_SERVO = 18; // T11 servo -> R9 -> U5 pin 2/3 -> R4 -> J1 SIG. 50 Hz pulses (MG996R).
constexpr uint8_t PIN_SENSE = 34; // T11 sense <- R5 100k / R6 18k from +24V_M, R15 100k pull-down (Rev E). HIGH = motion power present.
                                  //   Input only, no internal pull. LOW = E-stop pressed, F1 blown, PSU off or sense wire broken.

// Onboard blue LED of the ESP-32S NodeMCU board. Not part of the rig wiring.
// GPIO2 is a strapping pin: use it only for status blinks, never for rig functions.
constexpr uint8_t PIN_BOARD_LED = 2;
