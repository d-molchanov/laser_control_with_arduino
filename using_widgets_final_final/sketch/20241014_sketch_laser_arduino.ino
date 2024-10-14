#define GENPIN 2

int singlePulseMode;
volatile int periodicMode;
int continuousMode;

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
  // Проверяем, есть ли данные из Serial порта
  long timeStart;
  int fr;

  if (continuousMode == 1) {
    digitalWrite(GENPIN, HIGH);
    continuousMode = 0;
  }
  if (periodicMode == 1) {
    digitalWrite(GENPIN, LOW);
    periodicMode = 0;
  }

  if (Serial.available() > 0) {

    // Читаем полученные данные и сохраняем их в переменной
    String receivedData = Serial.readString();
    int n = receivedData.indexOf(':');
    String mode = receivedData.substring(0, 1);
    long timingData = receivedData.substring(1, n).toInt();
    int intensity = receivedData.substring(n + 1).toInt();
    controlPins(intensity);
    if (mode == "s") {
      singlePulseMode = 1;
      periodicMode = 0;
      continuousMode = 0;
      if (digitalRead(GENPIN)) {
        digitalWrite(GENPIN, LOW);
      }
      digitalWrite(GENPIN, HIGH);
      delayMicroseconds(timingData);
      // delay(timingData);
      digitalWrite(GENPIN, LOW);
      singlePulseMode = 0;
    }
    if (mode == "l") {
      singlePulseMode = 1;
      periodicMode = 0;
      continuousMode = 0;
      if (digitalRead(GENPIN)) {
        digitalWrite(GENPIN, LOW);
      }
      digitalWrite(GENPIN, HIGH);
      // delayMicroseconds(fr);
      delay(timingData);
      digitalWrite(GENPIN, LOW);
      singlePulseMode = 0;
    }
    if (mode == "p") {
      singlePulseMode = 0;
      periodicMode = 1;
      continuousMode = 0;
    }
    if (mode == "c") {
      singlePulseMode = 0;
      periodicMode = 0;
      continuousMode = 1;
      digitalWrite(GENPIN, HIGH);

      // // TCCR1B &= ~(1 << CS12);
      // if (continuousMode == 0) {
      //   // TCCR1B = 0;
      //   // TIMSK1 &= ~(1 << OCIE1A);
      //   // cli();  // отключить глобальные прерывания
      //   digitalWrite(GENPIN, HIGH);
      // }
    }
    if (mode == "t") {
      singlePulseMode = 0;
      periodicMode = 0;
      continuousMode = 0;
      digitalWrite(GENPIN, LOW);
      controlPins(3);
    }

    // setupTimer(fr);
    // Отправляем ответ обратно в Serial порт
    Serial.println("Mode:" + mode);
    // Serial.println("Mode:" + TCCR1B);
    Serial.println("Frequency:" + String(timingData));
    Serial.println("Intensity:" + String(intensity));
    // Serial.println("Received: " + String(n));
    // Serial.println("Received: " + receivedData + "\n");
    // Serial.print("\n");
  }
  // Serial.println("hello!");
  // delay(1000);
  // Serial.println(Serial.readString());
}

// void setupTimer(int frequency) {
//   // Serial.println("Timer was set up.");
//   float time_resolution = 1.6e-5;
//   int timer_counts = ceil(1.0/(2*frequency*time_resolution) - 1);
//   // инициализация Timer1
//   cli();  // отключить глобальные прерывания
//   TCCR1A = 0;   // установить регистры в 0
//   TCCR1B = 0;

//   // OCR1A = 15624; // установка регистра совпадения
//   // OCR1A = 624; // установка регистра совпадения
//   OCR1A = timer_counts; // установка регистра совпадения

//   TCCR1B |= (1 << WGM12);  // включить CTC режим
//   // TCCR1B |= (1 << CS10); // Установить биты на коэффициент деления 1024
//   // TCCR1B |= (1 << CS12);
//   TCCR1B |= (1 << CS12); // Установить биты на коэффициент деления 256

//   TIMSK1 |= (1 << OCIE1A);  // включить прерывание по совпадению таймера
//   sei(); // включить глобальные прерывания

// }

// #define OSP_SET_WIDTH(cycles) (OCR1B = 0xffff-(cycles-1))

// void setupTimerForPulse(uint8_t cycles) {
//   // Serial.println("Timer was set up.");
//   float time_resolution = 0.5e-6;
//   // int timer_counts = ceil(1.0/(2*duration*time_resolution) - 1);
//   // инициализация Timer1
//   cli();  // отключить глобальные прерывания
//   TCCR1A = 0;   // установить регистры в 0
//   TCCR1B = 0;

//   // OCR1A = 15624; // установка регистра совпадения
//   // OCR1A = 624; // установка регистра совпадения
//   OCR1A = 0; // установка регистра совпадения

//   TCCR1B |= (1 << WGM12);  // включить CTC режим
//   // TCCR1B |= (1 << CS10); // Установить биты на коэффициент деления 1024
//   // TCCR1B |= (1 << CS12);
//   TCCR1B |= (1 << CS11); // Установить биты на коэффициент деления 256

//   TIMSK1 |= (1 << OCIE1A);  // включить прерывание по совпадению таймера
//   sei(); // включить глобальные прерывания

// }

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

// ISR(TIMER1_COMPA_vect)
// {
//     if (periodicMode == 1) {
//       digitalWrite(GENPIN, !digitalRead(GENPIN));
//     }
// }