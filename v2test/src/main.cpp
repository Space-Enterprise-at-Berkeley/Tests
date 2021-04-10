#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include <string>
#include <vector>

using namespace std;

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire1);

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

// float drogue = 0;
// float main = 0;

// uint32_t time = 0;

void setup() {
  Serial.begin(57600);
  delay(1000);

  bno.begin();

  bno.setExtCrystalUse(true);
  bno.setAxisRemap(Adafruit_BNO055::REMAP_CONFIG_P7);
  // time = millis();
}

void loop() {
  imu::Quaternion quat = bno.getQuat();

  Serial.println(create_packet(15, {(float) quat.w() * 100000.0, (float) quat.x() * 100000.0, (float) quat.y() * 100000.0, (float) quat.z() * 100000.0}).c_str());

  // Serial.println(create_packet(14, {}))

  delay(10);

  // if(millis() - time > 10000) {
  //   drogue = 1;
  // }

  // if(millis() - time > 20000) {
  //   main = 1;
  // }

  // if(millis() - time > 30000) {
  //   time = millis();
  //   drogue = 0;
  //   main = 0;
  // }

  // Serial.println(create_packet(10, {drogue, main}).c_str());


  // delay(200);
  // Serial.println("test");
  // delay(1000);
}
