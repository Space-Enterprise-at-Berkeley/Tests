#include <ducer.h>
#include <Wire.h>

#define RESET_PIN_1 14
//#define RESET_PIN_2 8

void setup() {
  // put your setup code here, to run once:

  pinMode(RESET_PIN_1, OUTPUT);
//  pinMode(RESET_PIN_2, OUTPUT);
//
  digitalWrite(RESET_PIN_1, HIGH);
  
  Wire.begin();
  Serial.begin(9600);
  delay(1000);
  
  Ducers::init(&Wire);

  Serial.println("ADC 1 addr: ");
  Serial.println(Ducers::ADC1_ADDR, HEX);

  Serial.println("ADC 2 addr: ");
  Serial.println(Ducers::ADC2_ADDR, HEX);

    Serial.print("calibration 1:  ");
    Serial.println(Ducers::calibration1);


 Serial.print("calibration 2:  ");
    Serial.println(Ducers::calibration2);

    Serial.print("writing to reg 0 on ADC 2: ");
    Serial.println(Ducers::MUX_SEL_0 | Ducers::ADC_SETTINGS, BIN);
}
float data[6];
bool start = false;

void loop() {
  Serial.println("data ready: ");
  Serial.println(Ducers::isDataReady(Ducers::ADC1_ADDR));
  
  if (start){

  // put your main code here, to run repeatedly:
  Ducers::readPropaneTankPressure(data);
  Serial.print("propane tank: ");
  Serial.println(data[0]);

  Ducers::readLOXTankPressure(data);
  Serial.print("LOX tank: ");
  Serial.println(data[0]);

  Ducers::readPropaneInjectorPressure(data);
  Serial.print("propane Injector: ");
  Serial.println(data[0]);

  Ducers::readLOXInjectorPressure(data);
  Serial.print("LOX injector: ");
  Serial.println(data[0]);

  Ducers::readHighPressure(data);
  Serial.print("High pressure: ");
  Serial.println(data[0]);
  
  Serial.println("\n\n\n");

  delay(100);
  } else {
    if (Serial.available()){
      int serRead = Serial.read();
      if (serRead == '0') {
        start = true;
      }
    }
  }
  
}
