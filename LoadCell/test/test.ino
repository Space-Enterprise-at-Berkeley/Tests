#include "loadCell.h"


HX711 loadcells[2];

int numSensors = 2;
byte sckPins[] = {A1, A3};
byte doutPins[] = {A0, A2};
float calVals[] = {4000, -4000};
float curVals[3] = {};


void setup() {

  Serial.begin(9600);
  delay(5000);
  Serial.println("loadCell testing");
  Serial.flush();

  for (int i = 0; i < numSensors; i++) {
     loadcells[i].begin(doutPins[i], sckPins[i]);
     loadcells[i].set_scale(calVals[i]);
     loadcells[i].tare();

     long zero_factor = loadcells[i].read_average(); //Get a baseline reading
     Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
     Serial.println(zero_factor);
  }

  LoadCell::init(loadcells, numSensors, sckPins, doutPins, calVals);
  Serial.flush();
}

void loop() {

  LoadCell::readLoadCells(curVals);

  Serial.println("LoadCell 2:");
  Serial.println(curVals[0]);

  Serial.println("LoadCell 1:");
  Serial.println(curVals[1]);

  
//  for (int i = 0; i < numSensors; i++) {
//    Serial.print("LoadCell: ");
//    Serial.println(i);
//    Serial.println(curVals[i]);
//    Serial.println("Test");
//  }


}
