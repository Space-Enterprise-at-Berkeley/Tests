/*
 OpenLCD is an LCD with Serial/I2C/SPI interfaces.
 By: Nathan Seidle
 SparkFun Electronics
 Date: April 19th, 2015
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
 This is example code that shows how to send data over I2C to the display.
 Note: This code expects the display to be listening at the default I2C address. If your display is not at 0x72, you can
 do a hardware reset. Tie the RX pin to ground and power up OpenLCD. You should see the splash screen
 then "System reset Power cycle me" and the backlight will begin to blink. Now power down OpenLCD and remove
 the RX/GND jumper. OpenLCD is now reset.
 To get this code to work, attached an OpenLCD to an Arduino Uno using the following pins:
 SCL (OpenLCD) to A5 (Arduino)
 SDA to A4
 VIN to 5V
 GND to GND
 Command cheat sheet:
 ASCII / DEC / HEX
 '|'    / 124 / 0x7C - Put into setting mode
 Ctrl+c / 3 / 0x03 - Change width to 20
 Ctrl+d / 4 / 0x04 - Change width to 16
 Ctrl+e / 5 / 0x05 - Change lines to 4
 Ctrl+f / 6 / 0x06 - Change lines to 2
 Ctrl+g / 7 / 0x07 - Change lines to 1
 Ctrl+h / 8 / 0x08 - Software reset of the system
 Ctrl+i / 9 / 0x09 - Enable/disable splash screen
 Ctrl+j / 10 / 0x0A - Save currently displayed text as splash
 Ctrl+k / 11 / 0x0B - Change baud to 2400bps
 Ctrl+l / 12 / 0x0C - Change baud to 4800bps
 Ctrl+m / 13 / 0x0D - Change baud to 9600bps
 Ctrl+n / 14 / 0x0E - Change baud to 14400bps
 Ctrl+o / 15 / 0x0F - Change baud to 19200bps
 Ctrl+p / 16 / 0x10 - Change baud to 38400bps
 Ctrl+q / 17 / 0x11 - Change baud to 57600bps
 Ctrl+r / 18 / 0x12 - Change baud to 115200bps
 Ctrl+s / 19 / 0x13 - Change baud to 230400bps
 Ctrl+t / 20 / 0x14 - Change baud to 460800bps
 Ctrl+u / 21 / 0x15 - Change baud to 921600bps
 Ctrl+v / 22 / 0x16 - Change baud to 1000000bps
 Ctrl+w / 23 / 0x17 - Change baud to 1200bps
 Ctrl+x / 24 / 0x18 - Change the contrast. Follow Ctrl+x with number 0 to 255. 120 is default.
 Ctrl+y / 25 / 0x19 - Change the TWI address. Follow Ctrl+x with number 0 to 255. 114 (0x72) is default.
 Ctrl+z / 26 / 0x1A - Enable/disable ignore RX pin on startup (ignore emergency reset)
 '-'    / 45 / 0x2D - Clear display. Move cursor to home position.
        / 128-157 / 0x80-0x9D - Set the primary backlight brightness. 128 = Off, 157 = 100%.
        / 158-187 / 0x9E-0xBB - Set the green backlight brightness. 158 = Off, 187 = 100%.
        / 188-217 / 0xBC-0xD9 - Set the blue backlight brightness. 188 = Off, 217 = 100%.
 For example, to change the baud rate to 115200 send 124 followed by 18.
*/


#include <Wire.h>
#include <math.h>

#define DISPLAY_ADDRESS1 0x72 //This is the default address of the OpenLCD
#define RFSerial Serial1

int cycles = 0;
bool back_not_set = true;

bool packet_found = false;
bool reading = false;

char raw_data[100];

String LOX_tank = "";
String Prop_tank = "";

int color = 0;
int redVal, greenVal, blueVal, val;
int changed = 0;

void setup()
{
  
  

  
  
  Wire.begin(); //Join the bus as master

  //By default .begin() will set I2C SCL to Standard Speed mode of 100kHz
  //Wire.setClock(400000); //Optional - set I2C SCL to High Speed Mode of 400kHz

  RFSerial.begin(57600);
  Serial.begin(9600); //Start serial communication at 9600 for debug statements
  Serial.println("OpenLCD Example Code");

  //Send the reset command to the display - this forces the cursor to return to the beginning of the display
  Wire.beginTransmission(DISPLAY_ADDRESS1);
  Wire.write('|'); //Put LCD into setting mode
  Wire.write('-'); //Send clear display command
  Wire.endTransmission();

  redVal = 0;
  greenVal = 0;
  blueVal = 0;
  val = 0;
  color = "red";
}

void loop()
{

//  Serial.print("cyle ");
//  Serial.println(cycles);
  
  packet_found = false; 
//  if (RFSerial.available() > 0) {
//      int i = 0;
//      if (i == 0) {
//        packet_found = true;  
//      }
//      while(RFSerial.available() > 0) {
//        raw_data[i] = Serial.read();
//        i++;
//        if (raw_data[i] == "\n") {
//          break;
//        }
//        if (i == 99) {
//          break;  
//        }
//        Serial.print("testing ");
//        Serial.println(i);
//      }

//      char * data = decode_received_packet(String(raw_data));
//      
//        for (int i = 0; i < 10; i++) {
//          Serial.print(data[i]);  
//        }
//       
//   }
//  int i;
//  reading = false;
//  if (RFSerial.available() > 0) {
//        char readByte = RFSerial.read();
//        Serial.print(readByte);
//        if (!reading and String(readByte).equals("{")) {
//          reading = true;
//          i = 0;
//        }
//        while (reading) {
//          readByte = RFSerial.read();
//          if (String(readByte).equals("}")) {
//          reading = false;
//          }
//          Serial.print(readByte);
//          
//        }
//        Serial.println();
//        if (readByte == '\n') {
//          Serial.println();
//        } else {
//          
//          Serial.print(readByte);
//        }
//    }
  
  String packet = RFSerial.readStringUntil('\n');
  Serial.print(packet);
  Serial.println();
  int data_start_index = packet.indexOf(',');
  int valve_id = packet.substring(1,data_start_index).toInt();
  if (valve_id == 30) {
    int val1 = packet.indexOf(',') + 1;
    int val2 = 1+ val1 + packet.substring(val1+1).indexOf(',');
    int val3 = packet.indexOf('|');

//    Serial.print(val1);
//    Serial.print(",");
//    Serial.print(val2);
//     Serial.print(",");
//     Serial.println(val3);

    LOX_tank = packet.substring(val1,val2);
    Prop_tank = packet.substring(val2+1,val3);
//    Serial.print(Prop_tank.length());
  }

  delay(50);
  
  cycles++; //Counting cycles! Yay!
  //  Serial.print("Cycle: "); //These serial.print statements take multiple miliseconds
  //  Serial.println(cycles);
  
  blueVal = 0;//100*cos(2*cycles/M_PI) + 150;
  greenVal = 0;//100*cos(2*cycles/M_PI - 2*M_PI/3.0) + 150;
  redVal = 0;//125*cos(2*cycles/M_PI- 4*2*M_PI/3.0) + 130;
  val = 125*cos(2.0*cycles/M_PI) + 130;

  Serial.println(val);
  if (val < 12) {
    
     color = (color + 1) % 3;
     Serial.print("color ");
     Serial.println(color);
  
  }

  if (color == 0) {
    blueVal = val;
  } else if (color == 1) {
    greenVal = val;
  } else if (color == 2) {
    redVal = val;
  }

  

  i2cSendValue(LOX_tank,Prop_tank); //Send the four characters to the display
//  delay(50); //The maximum update rate of OpenLCD is about 100Hz (10ms). A smaller delay will cause flicker
}

//Given a number, i2cSendValue chops up an integer into four values and sends them out over I2C
void i2cSendValue(String word1, String word2)
{
  Wire.beginTransmission(DISPLAY_ADDRESS1); // transmit to device #1

  if (back_not_set) {
//    Serial.println("Mono/Red backlight set to 100%");
//    Wire.write('|');
//    Wire.write(128 + 0); //Set white/red 
//    Wire.write('|');
//    Wire.write(158 + 0); //Set green
//    Wire.write('|'); 
//    Wire.write(188 + 15); //Set blue
      Wire.write('|');
      Wire.write('+');
      Wire.write(0x00);
      Wire.write(0x00);
      Wire.write(0x00);
//    Wire.write(128 + 30*(value % 3) + 29); //Set white/red backlight amount to 100%
    back_not_set = false;
  }
//  Wire.write('|'); 
//  Wire.write(188 + blueVal); //Set blue
      Wire.write('|');
      Wire.write('+');
      Wire.write(redVal);
      Wire.write(greenVal);
      Wire.write(blueVal);
//      Serial.println(blueVal);
  
  Wire.write('|'); //Put LCD into setting mode
  Wire.write('-'); //Send clear display command

  Wire.print("LOX  Tank:");
  Wire.print(word1);
    for (int i = 0; i < (6-word1.length()); i++) {
    Wire.print(" ");
  }
  Wire.print("Prop Tank:");
  Wire.print(word2);
   for (int i = 0; i < (5-word2.length()); i++) {
    Wire.print(" ");
  }

//  delay(50);

  Wire.endTransmission(); //Stop I2C transmission
}


const char * decode_received_packet(String packet) {
  int data_start_index = packet.indexOf(',');
  int valve_id = packet.substring(1,data_start_index).toInt();
  const int data_end_index = packet.indexOf('|');
  int action = packet.substring(data_start_index + 1,data_end_index).toInt();
  
  String checksumstr = packet.substring(data_end_index + 1, packet.length()-2);
//  char checksum_char[5];
//  checksumstr.toCharArray(checksum_char, 5);
  char *checksum_char = checksumstr.c_str();
  uint16_t checksum = strtol(checksum_char, NULL, 16);
  
  char const *data = packet.substring(1,data_end_index).c_str();
  int count = data_end_index - 1; // sanity check; is this right? off by 1 error?
  uint16_t check = Fletcher16((uint8_t *) data, count);
  if (check == checksum) {
    return data;
  } else {
    return NULL;
  }
}

/*
 * Calculates checksum for key values being sent to ground station:
 * sensor_ID and it's corresponding data points
 */
uint16_t Fletcher16(uint8_t *data, int count) {
  
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
