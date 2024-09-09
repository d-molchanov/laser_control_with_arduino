// Arduino таймер CTC прерывание
// avr-libc library includes
#include <avr/io.h>
#include <avr/interrupt.h>
#define GENPIN 2

const int numPins = 13;
int inputValue;

void setup()
{

    Serial.begin(9600);
    for (int i = 2; i < 13; i++) {
      pinMode(i, OUTPUT);
    }
    int fr = 200;
    float res = 1.6e-5;
    int c = ceil(1.0/fr/res - 1);
    Serial.println("Частота на пине " + String(GENPIN) + ": " + String(fr) + " Гц");
    Serial.println("Значение регистра совпадения: " + String(c));
    // pinMode(GENPIN, OUTPUT);
    // инициализация Timer1
    cli();  // отключить глобальные прерывания
    TCCR1A = 0;   // установить регистры в 0
    TCCR1B = 0;

    // OCR1A = 15624; // установка регистра совпадения
    // OCR1A = 624; // установка регистра совпадения
    OCR1A = c; // установка регистра совпадения
    
    TCCR1B |= (1 << WGM12);  // включить CTC режим 
    // TCCR1B |= (1 << CS10); // Установить биты на коэффициент деления 1024
    // TCCR1B |= (1 << CS12);
    TCCR1B |= (1 << CS12); // Установить биты на коэффициент деления 256

    TIMSK1 |= (1 << OCIE1A);  // включить прерывание по совпадению таймера 
    sei(); // включить глобальные прерывания
}

void loop()
{
    // основная программа
    if (Serial.available() > 0){
      int n = Serial.parseInt();
      if (n < 3) {
        // Serial.println(n);
        n = 3;
      }
      if (n > 4095) {
        // Serial.println(n);
        n = 4095;
      }
      Serial.println(n);
      for (int i = 2; i < 12; i++){
        if ((n >> i) & 1) {
          digitalWrite(14 - i, HIGH);
          // Serial.println("Pin " + String(14-i) + ": 1");
        } else {
          digitalWrite(14 - i, LOW);
          // Serial.println("Pin " + String(14-i) + ": 0");
        }
        Serial.println("Pin " + String(14 - i) + ": " + digitalRead(14-i));
      }
    }
}

ISR(TIMER1_COMPA_vect)
{
    digitalWrite(GENPIN, !digitalRead(GENPIN));
}