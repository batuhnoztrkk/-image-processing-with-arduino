#include <Servo.h>

Servo servoM;
int ledPin = 13; // LED connected to digital pin 13


void setup() {
  pinMode(ledPin, OUTPUT); // sets the digital pin as output
  servoM.attach(9);
  Serial.begin(9600); // starts serial communication
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read(); // read the incoming byte
    if (command == '1') {
      digitalWrite(ledPin, HIGH); // turn the LED on
      for (pos = 0; pos <= 180; pos += 1) { // For döngüsü ile 0 ile 180 derece arası gitmesini sağladık.
        servoM.write(pos);              // Servo açı değeri olarak belirlediğimiz pos değişkenini servoya yazdırdık.
        delay(15);                       // servonun hedeflenen açıya gidebilmesi için 15 ms bekleme ekledik.
      }
    } else if (command == '0') {
      digitalWrite(ledPin, LOW); // turn the LED off
      for (pos = 180; pos >= 0; pos -= 1) { // for döngüsü ile 180 ile 0 derece arası gitmesini sağladık.
        servoM.write(pos);              // Servo açı değeri olan pos değişkenini servo’ya yazdırdık.
        delay(15);                       // Servonun açı değerine gidebilmesi için 15 ms. bekleme ekledik.
      }
    }
  }
}