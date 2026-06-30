#include <Servo.h>

Servo actuatorServo;

const int trigPin = 9;
const int echoPin = 10;
const int servoPin = 6;
const int ledPin = 3;

int servoAngle = 90;
int ledIntensity = 0;

float readDistanceCm() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  if (duration == 0) {
    return -1.0;
  }

  float distance = duration * 0.0343 / 2.0;
  return distance;
}

void applyAction(int angle, int intensity) {
  angle = constrain(angle, 20, 160);
  intensity = constrain(intensity, 0, 255);

  actuatorServo.write(angle);
  analogWrite(ledPin, intensity);
}

void setup() {
  Serial.begin(115200);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);

  actuatorServo.attach(servoPin);
  actuatorServo.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.startsWith("A,")) {
      int firstComma = line.indexOf(',');
      int secondComma = line.indexOf(',', firstComma + 1);

      if (secondComma > 0) {
        servoAngle = line.substring(firstComma + 1, secondComma).toInt();
        ledIntensity = line.substring(secondComma + 1).toInt();
        applyAction(servoAngle, ledIntensity);
      }
    }
  }

  float distance = readDistanceCm();
  Serial.print("S,");
  Serial.println(distance);

  delay(120);
}
