#include <TimerOne.h>
#define GENPIN 2
// #define GENPIN 12
// Message structure: "p4095:00010000:00010000:00200"


bool singlePulseModeUS;
bool singlePulseModeMS;
// volatile int periodicModeUS;
bool continuousMode;
bool periodicModeUS;
bool periodicModeMS;

bool timerRunning = false;
long i;
long count;

long intensity;
long pulseDuration;
long pauseDuration;
long iterations;

void generatePulseUS(long pulse, long pause) {
  digitalWrite(GENPIN, HIGH);
  // PORTB |= (1 << 4);
  delayMicroseconds(pulse);
  digitalWrite(GENPIN, LOW);
  // PORTB &= ~ (1 << 4);
  delayMicroseconds(pause);
}

void generatePulseMS(long pulse, long pause) {
  digitalWrite(GENPIN, HIGH);
  // PORTB |= (1 << 4);
  delay(pulse);
  digitalWrite(GENPIN, LOW);
  // PORTB &= ~ (1 << 4);
  delay(pause);
}

void setup() {
  // Начинаем работу с Serial портом на скорости 9600 бит/с
  Serial.begin(9600);
  Serial.setTimeout(50);
  for (int i = 2; i < 13; i++) {
    pinMode(i, OUTPUT);
  }
  delay(1000);
  controlPins(3);
}

void loop() {
  if (periodicModeUS) {
    if (i < iterations) {
      generatePulseUS(pulseDuration, pauseDuration);
      i++;
    } else {
      periodicModeUS = false;
    }
  }
  if (periodicModeMS) {
    if (i < iterations) {
      generatePulseMS(pulseDuration, pauseDuration);
      i++;
    } else {
      periodicModeMS = false;
    }
  }
  if (continuousMode) {
    digitalWrite(GENPIN, HIGH);
    continuousMode = false;
  }
  if (singlePulseModeUS) {
    generatePulseUS(pulseDuration, pauseDuration);
    singlePulseModeUS = false;
  }
  if (singlePulseModeMS) {
    generatePulseMS(pulseDuration, pauseDuration);
    singlePulseModeMS = false;
  }
  if (Serial.available() > 0) {
    digitalWrite(GENPIN, LOW);
    count = 0;
    String receivedData = Serial.readString();
    String mode = receivedData.substring(0, 1);
    if (mode == "t") {
      controlPins(3);
      singlePulseModeUS = false;
      singlePulseModeMS = false;
      periodicModeUS = false;
      periodicModeMS = false;
      continuousMode = false;
      pulseDuration = 0;
      pauseDuration = -1;
      iterations = 0;
    } else {
      intensity = receivedData.substring(1, 5).toInt();
      pulseDuration = receivedData.substring(6, 14).toInt();
      pauseDuration = receivedData.substring(15, 23).toInt();
      iterations = receivedData.substring(24, 31).toInt();
      controlPins(intensity);
      if (mode == "s") {
        singlePulseModeUS = true;
        singlePulseModeMS = false;
        periodicModeUS = false;
        periodicModeMS = false;
        continuousMode = false;
        iterations = 1;
      }
      if (mode == "l") {
        singlePulseModeUS = false;
        singlePulseModeMS = true;
        periodicModeUS = false;
        periodicModeMS = false;
        continuousMode = false;
        iterations = 1;
      }
      if (mode == "p") {
        singlePulseModeUS = false;
        singlePulseModeMS = false;
        periodicModeUS = true;
        periodicModeMS = false;
        continuousMode = false;
        timerRunning = true;
        i = 0;
      }
      if (mode == "m") {
        singlePulseModeUS = false;
        singlePulseModeMS = false;
        periodicModeUS = false;
        periodicModeMS = true;
        continuousMode = false;
        timerRunning = true;
        i = 0;
      }
      if (mode == "c") {
        singlePulseModeUS = false;
        singlePulseModeMS = false;
        periodicModeUS = false;
        periodicModeMS = false;
        continuousMode = true;
        iterations = -1;
      }
      // Serial.println("Mode: " + mode);
      // Serial.println("Intensity: " + String(intensity));
      // Serial.println("Pulse duration: " + String(pulseDuration) + " us");
      // Serial.println("Pause duration: " + String(pauseDuration) + " us");
      // Serial.println("Iterations: " + String(iterations));
      // Serial.println("Checked intensity: " + String(checkPins()));
    }
    Serial.println(mode + ";" + String(checkPins()) + ";" + String(pulseDuration) + ";" + String(pauseDuration) + ";" + String(iterations));
  }

}

void controlPins(int value) {
  if (value < 3) {
    value = 3;
  }
  if (value > 4095) {
    value = 4095;
  }
  for (int i = 2; i < 12; i++) {
    if ((value >> i) & 1) {
      digitalWrite(14 - i, HIGH);
    } else {
      digitalWrite(14 - i, LOW);
    }
  }
}

int checkPins() {
  int result = 0;
  for (int i = 3; i < 13; i++) {
    result <<= 1;
    result += digitalRead(i);
  }
  result <<= 2;
  result += 3;
  return result;
}

