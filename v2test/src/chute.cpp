#include <Arduino.h>

#include <string>
#include <vector>

using namespace std;

uint16_t checksum(uint8_t *data, int count) {
  uint16_t sum1 = 0;
  uint16_t sum2 = 0;
  for (int index=0; index<count; index++) {
    if (data[index] > 0) {
      sum1 = (sum1 + data[index]) % 255;
      sum2 = (sum2 + sum1) % 255;
    }
  }
  return (sum2 << 8) | sum1;
}

string create_packet(int id, vector<float> args) {
  // send packet
  string raw_packet = "" + string(((String)id).c_str());
  for(float e : args) {
    raw_packet += "," + string(((String)e).c_str());
  }
  uint16_t raw_checksum = checksum((uint8_t *)raw_packet.c_str(), raw_packet.length());
  char c_checksum[5];
  sprintf(c_checksum, "%x", raw_checksum);
  raw_packet += "|" + string(c_checksum);
  raw_packet = "{" + raw_packet + "}";
  return raw_packet;
}

float drogue;
float deek;

uint32_t time;

void setup() {
    Serial.begin(57600);
    delay(1000);

    time = millis();
    drogue = 0.0;
    deek = 0.0;
}

void loop() {
    uint32_t now = millis();
    if(now - time > 10000) {
    drogue = 1.0;
  }

  if(now - time > 20000) {
    deek = 1.0;
  }

  if(now - time > 30000) {
    time = now;
    drogue = 0.0;
    deek = 0.0;
  }

  Serial.println(create_packet(10, {drogue, deek}).c_str());
// Serial.println("test");


  delay(200);
}
