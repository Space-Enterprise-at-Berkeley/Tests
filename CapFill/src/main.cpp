#include <Arduino.h>
#include <CapacitiveSensor.h>
#include <string>

/*
 * CapitiveSense Library Demo Sketch
 * Paul Badger 2008
 * Uses a high value resistor e.g. 10 megohm between send pin and receive pin
 * Resistor effects sensitivity, experiment with values, 50 kilohm - 50 megohm. Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 * Best results are obtained if sensor foil and wire is covered with an insulator such as paper or plastic sheet
 */

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

void handle_packet(int id, float value) {
  // send packet
  String raw_packet = "" + (String)id;
  raw_packet += "," + (String)value;
  uint16_t raw_checksum = checksum((uint8_t *)raw_packet.c_str(), raw_packet.length());
  char c_checksum[5];
  sprintf(c_checksum, "%x", raw_checksum);
  raw_packet += "|" + String(c_checksum);
  raw_packet = "{" + raw_packet + "}";
  Serial.println(raw_packet);
}


CapacitiveSensor   cs_4_2 = CapacitiveSensor(7,6);        // 10 megohm resistor between pins 4 & 2, pin 2 is sensor pin, add wire, foil

void setup()                    
{
   cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);     // turn off autocalibrate on channel 1 - just as an example
   Serial.begin(9600);
}

void loop()                    
{
    long start = millis();
    long total1 =  cs_4_2.capacitiveSensor(30);
    
    handle_packet(0, millis() - start);
    handle_packet(1, total1/30.0);          // per read value

    delay(200);                             // arbitrary delay to limit data to serial port 
}