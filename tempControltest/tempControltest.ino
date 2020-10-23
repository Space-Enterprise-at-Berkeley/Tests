#include <tempController.h>
#include <Thermocouple.h>
#include <math.h>

#define heaterPin 7
#define testPin 2


float data[2];
int heaterStatus = LOW;
int voltageOut = 0;

int amp = 128;
float T = 25 * 1000;
int testVoltage = 0;

long startMillis;

void setup() {
  startMillis = millis();
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(heaterPin, OUTPUT);

  pinMode(testPin, OUTPUT);

//  pinMode(4, OUTPUT);
//  analogWrite(4, 150);
  
//  digitalWrite(heaterPin, heaterStatus);
//  digitalWrite(heaterPin, HIGH);
  Thermocouple::init(1, 11);
  Thermocouple::setSensor(0);
  tempController::init(20, 2); 
}

void loop() {
  // put your main code here, to run repeatedly:
  Thermocouple::setSensor(0);
  Thermocouple::readTemperatureData(data);
  voltageOut = tempController::controlTemp(data[0]);
  analogWrite(heaterPin, voltageOut);

  //Serial.print("temperature: ");
  Serial.print(data[0]);
  Serial.print(", ");
  Serial.println(voltageOut);
  delay(100);
}
