#include <solenoids.h>
//#include <Wire.h>

Solenoids valves; // = new Solenoids();

void setup() {

  Serial.begin(9600);
  valves.init();
}

void loop() {
  if (Serial.available() > 0) {
      int readByte = Serial.read();
      if(readByte == 'a') {
        Serial.print("Toggled LOX 2: ");
        Serial.println(valves.toggleLOX2Way());
      } else if(readByte == 'b') {
        Serial.print("Toggled LOX 5: ");
        Serial.println(valves.toggleLOX5Way());
      } else if (readByte == 'c') {
        Serial.print("Toggled LOX Gems: ");
        Serial.println(valves.toggleLOXGems());
      } else if(readByte == 'x') {
        Serial.print("Toggled PROP 2: ");
        Serial.println(valves.toggleProp2Way());
      } else if (readByte == 'y') {
        Serial.print("Toggled PROP 5: ");
        Serial.println(valves.toggleProp5Way());
      } else if (readByte == 'z') {
        Serial.print("Toggled PROP Gems: ");
        Serial.println(valves.togglePropGems());
      }
    }
    delay(100);
}
