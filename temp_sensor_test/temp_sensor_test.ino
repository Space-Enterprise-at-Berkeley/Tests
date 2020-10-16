#include <Thermocouple.h>
#include <Arduino.h>

float reading1 = 0;
float reading2 = 0;
float reading3 = 0;
float data[6];

void setup() {
  // put your setup code here, to run once:
  //sensor  = Thermocouple(1);
  Thermocouple::init(3);
  Serial.begin(9600);
  delay(50);
  Serial.println("Started");
}

void loop() {
  // put your main code here, to run repeatedly:
  Thermocouple::readTemperatureData(data, 0);
  reading1 = data[0];

  Serial.print("temp1: ");
  Serial.print(reading1);
  Serial.print(" deg C, ROM1: ");
  for (int i = 0; i < 8; i++){
    Serial.print(Thermocouple::rom[i]);
  }
  Serial.println("");
  Thermocouple::readTemperatureData(data, 1);
  reading2 = data[0];
  Serial.print("temp2: ");
  Serial.print(reading2);
  Serial.print(" deg C, ROM2: ");
  for (int i = 0; i < 8; i++){
    Serial.print(Thermocouple::rom[i]);
  }
  Serial.println("");
  Thermocouple::readTemperatureData(data, 2);
  reading3 = data[0];
  
  Serial.print("temp3: ");
  Serial.print(reading3);
  Serial.print(" deg C, ROM3: ");
  for (int i = 0; i < 8; i++){
    Serial.print(Thermocouple::rom[i]);
  }
  Serial.println("\n\n");
}
