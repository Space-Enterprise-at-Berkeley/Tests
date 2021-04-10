#include "Arduino.h"

#include <NativeEthernet.h>
#include <NativeEthernetUdp.h>

#include <string>

using namespace std;

EthernetUDP Udp;
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
unsigned int port = 42069; // try to find something that can be the same on gs
IPAddress groundIP(10, 0, 0, 69);
IPAddress ip(10, 0, 0, 178);

bool setupEthernetComms(byte * mac, IPAddress ip){
  Ethernet.begin(mac, ip);

  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    Serial.flush();
    exit(1);
  } else if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected.");
    Serial.flush();
    exit(1);
  }

  Udp.begin(port);
  return true;
}

void sendEthPacket(string packet){
  Udp.beginPacket(groundIP, port);
  Udp.write(packet.c_str());
  Udp.endPacket();
}

void setup() {
    Serial.begin(57600);
    delay(1000);

    setupEthernetComms(mac, ip);
}

void loop() {
    Serial.println("Sending ethernet packet");
    sendEthPacket("yeet");

    delay(500);
}
