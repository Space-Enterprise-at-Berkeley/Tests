#include <Arduino.h>
#include <vector>

#include "Packet.h"

#define RFSerial Serial6

vector<float> vals;

uint32_t counter;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  RFSerial.begin(57600);

  counter = 1;
}

void loop() {
  // put your main code here, to run repeatedly:
  vals.assign(1,counter);
  Serial.println(Packet::create_packet(16,vals).c_str());
  RFSerial.println(Packet::create_packet(16,vals).c_str());
  counter++;
  delay(200);

}