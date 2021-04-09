/*
  Automation.h - A c++ library including automated sequences triggered by
  commands or particular events (e.g. end of flow, overpressurization)
*/

#include "Packet.h"

using namespace std;

namespace Packet {

//-----------------------Variables-----------------------



//-----------------------Functions-----------------------

  
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

  
} //Packet