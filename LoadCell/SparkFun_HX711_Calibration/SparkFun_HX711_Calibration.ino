/*
 Basic Load Cell Operation in Kg
 Arduino pins
 5V -> VCC
 3.3V -> VDD
 3 -> DAT  NANO -> A0
 2 -> CLK  NANO -> A1
 GND -> GND
  
*/

#include "HX711.h" //This library can be obtained here http://librarymanager/All#Avia_HX711

#define LOADCELL_DOUT_PIN  A0
#define LOADCELL_SCK_PIN  A1

HX711 scale;

//float calibration_factor = -3950; // LC1 AMP1

//float calibration_factor = 3800; // LC2 AMP1
float calibration_factor = 4000; // LC2 AMP3

//float calibration_factor = -4000; // LC1 AMP3

void setup() {
  Serial.begin(9600);
  delay(3000);
  Serial.print("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press + or a to increase calibration factor");
  Serial.println("Press - or z to decrease calibration factor");
  Serial.flush(); //need this to print above statements

  Serial.println(LOADCELL_DOUT_PIN);
  Serial.println(LOADCELL_SCK_PIN);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale();
  scale.tare();  //Reset the scale to 0

  long zero_factor = scale.read_average(); //Get a baseline reading
  Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
}

void loop() {

  scale.set_scale(calibration_factor); //Adjust to this calibration factor

  Serial.print("Reading: ");
  Serial.print(scale.get_units() * 0.453592, 1);
  Serial.print(" kg"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();

  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+' || temp == 'a')
      calibration_factor += 10;
    else if(temp == '-' || temp == 'z')
      calibration_factor -= 10;
  }
}
