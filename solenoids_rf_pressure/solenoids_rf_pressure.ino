#include <math.h>
#include <solenoids.h>
#include <Wire.h>

#define LOW_PRESSURE_1 A0
#define LOW_PRESSURE_2 A1
#define LOW_PRESSURE_3 A2
#define LOW_PRESSURE_4 A3

#define HIGH_PRESSURE_1 A4
#define HIGH_PRESSURE_2 A5

#define RFSerial Serial8

void readData();
void convertData();

int input = 0;
bool shouldPrint = true;

long currTime = millis();
long currTime2 = millis();

int numLowPressure = 0;
int numHighPressure = 0;

/*
 * Template_I2C.ino - A c++ program that uses I2C communication to receive requests
 * for data from Brain_I2C.ino and send the corresponding data back.
 * Created by Vainavi Viswanath, Aug 21, 2020.
 */
#include <Wire.h>

/*
 * Change this address according to the board address this code is uploaded on
 */
int Address = 8;

int sensorNum = 0;
void (*generalFunc)(float*);

void setup() {
  Wire.begin(Address);
  Wire.onRequest(requestEvent);
  Wire.onReceive(updateSensorNum);
  Serial.begin(9600);
}

void loop() {
  delay(100);
}

/*
 * Data structure to allow the conversion of bytes to floats and vice versa.
 */
union floatArrToBytes {
  char buffer[24];
  float sensorReadings[6];
} farrbconvert;

/*
 * When a request comes from the brain, collects data from the requested sensor
 * and sends back float array with data points.
 */
void requestEvent() {
  float data[6] = {0,0,0,0,0,0};
  generalFunc(data);
  for (int i=0; i<6; i++) {
    farrbconvert.sensorReadings[i] = data[i];
  }
  Wire.write(farrbconvert.buffer, 24);
}

/*
 * Selects the corresponding function to the sensor which data is requested from.
 */
void updateSensorNum(int howMany) {
  while (!Wire.available());
  sensorNum = Wire.read();
  if (sensorNum == 0) {
    generalFunc = &getReading0;
  } else if (sensorNum == 1) {
    generalFunc = &getReading1;
  }
}

/*
 * Method to collect data from ______
 */
void getReading0(float *data) {
  //get the sensor reading here
  data[0] = 36.89;
  data[1] = 25.50;
  data[2] = 30.45;
}

/*
 * Method to collect data from ______
 */
float getReading1(float *data) {
  //get the sensor reading here
  data[0] = 14.26;
}



void setup() {

  Wire.begin(8);

  //If connected to RF, change baud rate from 9600 to 57600
  Serial.begin(57600);

  // Setup solenoids


  Serial.println("How many low pressure sensors are connected?");
  while (Serial.available() == 0) {

      delay(50);
      if (millis() - currTime > 2000) {
        Serial.println("waiting for low pt #...");
        currTime = millis();
      }
    }
  numLowPressure = Serial.parseInt();

//  numLowPressure = Serial.read() - 48;

Serial.println("How many high pressure sensors are connected?");
  while (Serial.available() == 0) {
      delay(50);
      if (millis() - currTime > 2000) {
        Serial.println("waiting for high pt #...");
        currTime = millis();
      }
    }

  numHighPressure = Serial.parseInt();

  Serial.print("There are ");
  Serial.print(numLowPressure);
  Serial.print(" low PTs and ");
  Serial.print(numHighPressure);
  Serial.println(" high PTs");

  if(numLowPressure >= 1){
    pinMode(LOW_PRESSURE_1, INPUT);
  }
  if(numLowPressure >= 2){
    pinMode(LOW_PRESSURE_2, INPUT);
  }
  if(numLowPressure >= 3){
    pinMode(LOW_PRESSURE_3, INPUT);
  }
  if(numLowPressure >= 4){
    pinMode(LOW_PRESSURE_4, INPUT);
  }
  if(numHighPressure >= 1){
    pinMode(HIGH_PRESSURE_1, INPUT);
  }
  if(numHighPressure >= 2){
    pinMode(HIGH_PRESSURE_2, INPUT);
  }

  Serial.print("high, lox tank, propane tank, lox injector, propane injector\n");

  currTime = millis();
  currTime2 = millis();
}

// 0.88V - 4.4V : ?? - 5000 PSI

int lowPressure1, lowPressure2, lowPressure3, lowPressure4, highPressure1, highPressure2;
int convertedLow1, convertedLow2, convertedLow3, convertedLow4, convertedHigh1, convertedHigh2;

int periodic = 100; // take data 10 times a second.
void loop() {
  currTime = millis();
  if((currTime%int(periodic)) == 0) {
//    if (Serial.available() > 0) {
//      int readByte = Serial.read();
//      if(readByte == 'a') {
//        Serial.print("Toggled LOX 2: ");
//        Serial.println(valves.toggleLOX2Way());
//      } else if(readByte == 'b') {
//        Serial.print("Toggled LOX 5: ");
//        Serial.println(valves.toggleLOX5Way());
//      } else if (readByte == 'c') {
//        Serial.print("Toggled LOX Gems: ");
//        Serial.println(valves.toggleLOXGems());
//      } else if(readByte == 'x') {
//        Serial.print("Toggled PROP 2: ");
//        Serial.println(valves.toggleProp2Way());
//      } else if (readByte == 'y') {
//        Serial.print("Toggled PROP 5: ");
//        Serial.println(valves.toggleProp5Way());
//      } else if (readByte == 'z') {
//        Serial.print("Toggled PROP Gems: ");
//        Serial.println(valves.togglePropGems());
//      } else if (readByte == 'e') {
//        Serial.print("Toggled High Pressure: ");
//        Serial.println(valves.toggleHighPressureSolenoid());
//      }
//    }

    readData();

//    convertData();

    //need some check on magnitude of reading to see if we should print data.
    if(shouldPrint){

      if(numHighPressure >= 1){
        //sprintf(toWriteBuffer + bufferIndex, "%d,", convertedHigh1);
        //bufferIndex += String(convertedHigh1).length();
        Serial.print(highPressure1);
      } else {
        Serial.print("-1");
      }
//      if(numHighPressure >= 2){
//        //sprintf(toWriteBuffer + bufferIndex, "%d,", convertedHigh2);
//        //bufferIndex += String(convertedHigh2).length();
//        Serial.print(", ");
//        Serial.print(convertedHigh2);
//      }

      Serial.print(", ");
      if(numLowPressure >= 1){
        Serial.print(lowPressure1);
        //Serial.println("Added first low PT reading;
      } else {
        Serial.print("-1");
      }

      Serial.print(", ");
      if(numLowPressure >= 2){
        //sprintf(toWriteBuffer + bufferIndex, "%d,", convertedLow2);
        //bufferIndex += String(convertedLow2).length();
        Serial.print(lowPressure2);
      } else {
        Serial.print("-1");
      }

      Serial.print(", ");
      if(numLowPressure >= 3){
        //sprintf(toWriteBuffer + bufferIndex, "%d,", convertedLow3);
        //bufferIndex += String(convertedLow3).length();
        Serial.print(lowPressure3);
      } else {
        Serial.print("-1");
      }

      Serial.print(", ");
      if(numLowPressure >= 4){
        //sprintf(toWriteBuffer + bufferIndex, "%d,", convertedLow4);
        //bufferIndex += String(convertedLow4).length();
        Serial.print(lowPressure4);
      } else {
        Serial.print("-1");
      }
      Serial.print("\n");
    }
  }
}

void convertData(){
    switch(numLowPressure){
    case 1:
      convertedLow1 = lowPressureConversion(lowPressure1);
      break;
    case 2:
      convertedLow1 = lowPressureConversion(lowPressure1);
      convertedLow2 = lowPressureConversion(lowPressure2);
      break;
    case 3:
      convertedLow1 = lowPressureConversion(lowPressure1);
      convertedLow2 = lowPressureConversion(lowPressure2);
      convertedLow3 = lowPressureConversion(lowPressure3);
      break;
    case 4:
      convertedLow1 = lowPressureConversion(lowPressure1);
      convertedLow2 = lowPressureConversion(lowPressure2);
      convertedLow3 = lowPressureConversion(lowPressure3);
      convertedLow4 = lowPressureConversion(lowPressure4);
      break;
  }

  switch(numHighPressure){
    case 1:
      convertedHigh1 = highPressureConversion(highPressure1);
      break;
    case 2:
      convertedHigh1 = highPressureConversion(highPressure1);
      convertedHigh2 = highPressureConversion(highPressure2);
      break;
  }
}

void readData(){
  switch(numLowPressure){
    case 1:
      lowPressure1 = analogRead(LOW_PRESSURE_1);
      break;
    case 2:
      lowPressure1 = analogRead(LOW_PRESSURE_1);
      lowPressure2 = analogRead(LOW_PRESSURE_2);
      break;
    case 3:
      lowPressure1 = analogRead(LOW_PRESSURE_1);
      lowPressure2 = analogRead(LOW_PRESSURE_2);
      lowPressure3 = analogRead(LOW_PRESSURE_3);
      break;
    case 4:
      lowPressure1 = analogRead(LOW_PRESSURE_1);
      lowPressure2 = analogRead(LOW_PRESSURE_2);
      lowPressure3 = analogRead(LOW_PRESSURE_3);
      lowPressure4 = analogRead(LOW_PRESSURE_4);
      break;
  }

  switch(numHighPressure){
    case 1:
      highPressure1 = analogRead(HIGH_PRESSURE_1);
      break;
    case 2:
      highPressure1 = analogRead(HIGH_PRESSURE_1);
      highPressure2 = analogRead(HIGH_PRESSURE_2);
      break;
  }
}


float lowPressureConversion(int raw){
  return int(1.2258857538273733*raw - 123.89876445934394);
}

float highPressureConversion(int raw){
//    return -9083 + (1.239 * pow(10,2) * raw) - 7.17 * pow(10,-1) * pow(raw, 2) + 2.29 * pow(10,-3) * pow(raw, 3);
    float converted = (((float)raw / 1024) - 0.2) * 5000;
    return converted;
//    return -11.3 + 1.53 * converted - 1.0327 * pow(10, -3) * pow(converted, 2) + 1.246 * pow(10, -6) * pow(converted,3);

}
