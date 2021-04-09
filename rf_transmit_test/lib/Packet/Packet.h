/*
  Packet.h - A c++ library including functions that can be used to easily 
  create and parse packets of the format {id,data....,CHKSUM}
*/


#ifndef __Packet__
#define __Packet__

#include <Arduino.h>
#include <string>
#include <vector>

using namespace std;

namespace Packet {

//-----------------------Variables-----------------------


//------------------------Structs------------------------


//------------------Function Definitions-----------------

  string create_packet(int id, vector<float> args);

  uint16_t checksum(uint8_t *data, int count);  
  
}

#endif
