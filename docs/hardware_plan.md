# Hardware Plan

## Minimum Hardware

```text
Arduino Uno / Nano / ESP32
HC-SR04 ultrasonic distance sensor
SG90 servo motor
LED
220Ω resistor
breadboard
jumper wires
USB cable
```

## Suggested Wiring for Arduino Uno

### HC-SR04

```text
VCC  -> 5V
GND  -> GND
TRIG -> D9
ECHO -> D10
```

### SG90 Servo

```text
Signal -> D6
VCC    -> 5V external recommended
GND    -> common GND
```

### LED

```text
D3 -> 220Ω resistor -> LED anode
LED cathode -> GND
```

## Serial Protocol

Python sends:

```text
A,<servo_angle>,<led_intensity>
```

Arduino returns:

```text
S,<distance_cm>
```
