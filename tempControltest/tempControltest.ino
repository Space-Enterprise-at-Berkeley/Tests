#include <tempController.h>
#include <Thermocouple.h>

#define heaterPin 2

float data[2];
int heaterStatus = LOW;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(heaterPin, OUTPUT);
  digitalWrite(heaterPin, heaterStatus);
  Thermocouple::init(1);
  tempController::init(10, 1); // set at 10 deg C with naive controller
}


void loop() {
  // put your main code here, to run repeatedly:
  Thermocouple::readTemperatureData(data, 0);
  heaterStatus = tempController::controlTemp(int(data[0]));
  digitalWrite(heaterPin, heaterStatus);
  Serial.print("temperature: ");
  Serial.print(data[0]);
  Serial.print(" deg C, heater is ");
  Serial.println(heaterStatus);
  delay(1000);
}
