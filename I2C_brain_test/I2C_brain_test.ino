#include <Wire.h>

void setup()
{
  Wire.begin(); // join i2c bus (address optional for master)
  //Wire.setSDA(18);
  //Wire.setSCL(19);
  Serial.begin(9600);
}

byte x = 5;

void loop()
{
  Serial.println("beginning transmission");
  Wire.beginTransmission(9); // transmit to device #9
  Serial.println("writing data");
  //Wire.write("x is ");        // sends five bytes
  Serial.println(5);
  Wire.write(5);              // sends one byte  
  Serial.println("finished transmission");
  Wire.endTransmission();    // stop transmitting

  delay(1000);
}


//#include <Arduino.h>
//#include <i2c_device.h>
//#include <i2c_driver_wire.h>
//
//void setup()
//{
//
//  // Enable the serial port for debugging
//  Serial.begin(9600);
//  Serial.println("Started");
//  Wire1.begin();
//}
//
//void loop()
//{
//  Serial.println("transmitting");
//  Wire1.beginTransmission(4); // transmit to device #4
//  Wire1.write("hello");        // sends five bytes
//  Serial.println(5);
//  Wire1.write(5);
//  Wire1.endTransmission();    // stop transmitting
//  delay(500);
//}
