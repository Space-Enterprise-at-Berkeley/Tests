#include <Thermocouple.h>
#include <typeinfo>

const int numCryoTherms = 2;
int cryoThermAddrs[numCryoTherms] = {0x60, 0x67}; // 0x6A, 0x6Ethe second one is 6A or 6B, not sure which for Addr pin set to 1/2


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500);
  
  Thermocouple::Cryo::init(numCryoTherms, cryoThermAddrs);
  Serial.println("finish init");
}

float data[6];
void loop() {
  // put your main code here, to run repeatedly:
  Thermocouple::Cryo::readCryoTemps(data);
  Serial.print("data: ");
  for (int i = 0; i < 6; i ++){
    Serial.print(String(data[i]) + ", ");
  }
  Serial.println();
  delay(100);

}
