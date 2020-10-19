#include <tempController.h>
#include <Thermocouple.h>
#include <math.h>

#define heaterPin 4
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
  
  digitalWrite(heaterPin, heaterStatus);
  digitalWrite(heaterPin, HIGH);
  Thermocouple::init(1);
  tempController::init(20, 2); // set at 10 deg C with naive controller
}


void loop() {
  // put your main code here, to run repeatedly:
  Thermocouple::readTemperatureData(data, 0);
  voltageOut = tempController::controlTemp(int(data[0]));
//   heaterStatus = HIGH;
  analogWrite(heaterPin, voltageOut);
  Serial.print("temperature: ");
  Serial.print(data[0]);
  Serial.print(" deg C, heater is ");
  Serial.println(voltageOut);

  testVoltage = amp * sin((float)(millis() - startMillis) * 2.0 * PI / T) + amp;
  analogWrite(testPin, testVoltage);
  Serial.print("PWM OUTPUT: ");
  Serial.println(testVoltage);

//  if(Serial.available()){

//    int r1 = Serial.read();
//    int r2 = Serial.read();
//    int r3 = Serial.read();
//    Serial.print(r1);
//    Serial.print(r2);
//    Serial.println(r3);
//    int red = (atoi(r1) * 100) + (atoi(r2) * 10) + (atoi(r3) * 1);
//
//    Serial.println(red);
//    //int val = atoi(mess);
//    analogWrite(testPin, red);
//    Serial.print("test pint output: ");
//    Serial.println(red);
//  }
  //delay(1000);
}
