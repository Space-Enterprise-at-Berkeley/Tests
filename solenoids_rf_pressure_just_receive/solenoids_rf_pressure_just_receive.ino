#include <math.h>
#include <solenoids.h>
#include <INA226.h> // https://github.com/jarzebski/Arduino-INA226
#include <tempController.h>
#include <Thermocouple.h>
#include <batteryMonitor.h>

#define heaterPin 7

#define RFSerial Serial6
#define arduino Serial3

INA226 ina;

void readData();
void convertData();

int input = 0;
bool shouldPrint = true;

long currTime = millis();

int numLowPressure = 0;
int numHighPressure = 0;

float data[2];
int voltageOut = 0;

float v, i;

void setup() {
  //If connected to RF, change baud rate from 9600 to 57600
  RFSerial.begin(57600);
  Serial.begin(9600);
  arduino.begin(9600);

  // Setup solenoids
  Solenoids::init();

  ina.begin();

  // Configure INA226
  ina.configure(INA226_AVERAGES_1, INA226_BUS_CONV_TIME_1100US, INA226_SHUNT_CONV_TIME_1100US, INA226_MODE_SHUNT_BUS_CONT);

  // Calibrate INA226. Rshunt = 0.01 ohm, Max excepted current = 4A
  ina.calibrate(0.002, 10);

  currTime = millis();

  pinMode(heaterPin, OUTPUT);

  Thermocouple::init(1, 11);
  Thermocouple::setSensor(0);
  tempController::init(20, 2); 
  
  Serial.println("started");
}

int periodic = 100; // take data 10 times a second.
void loop() {
  currTime = millis();
  if (RFSerial.available() > 0) {
    int readByte = RFSerial.read();
    Serial.print("Rf input: ");
    Serial.println(readByte);
    if(readByte == 'a') {
//      Serial.print("Toggled LOX 2: ");
      Serial.println(Solenoids::toggleLOX2Way());
    } else if(readByte == 'b') {
      Serial.print("Toggled LOX 5: ");
      Serial.println(Solenoids::toggleLOX5Way());
    } else if (readByte == 'c') {
      Serial.print("Toggled LOX Gems: ");
      Serial.println(Solenoids::toggleLOXGems());
    } else if(readByte == 'x') {
      Serial.print("Toggled PROP 2: ");
      Serial.println(Solenoids::toggleProp2Way());
    } else if (readByte == 'y') {
      Serial.print("Toggled PROP 5: ");
      Serial.println(Solenoids::toggleProp5Way());
    } else if (readByte == 'z') {
      Serial.print("Toggled PROP Gems: ");
      Serial.println(Solenoids::togglePropGems());
    } else if (readByte == 'e') {
      Serial.print("Toggled High Pressure: ");
      Serial.println(Solenoids::toggleHighPressureSolenoid());
    }
  }

  Thermocouple::setSensor(0);
  Thermocouple::readTemperatureData(data);
  voltageOut = tempController::controlTemp(data[0]);
  analogWrite(heaterPin, voltageOut);

  arduino.print(data[0]); // temp reading
  arduino.print(", ");
  arduino.print(voltageOut); // heater voltage
  arduino.print(", ");
//    Serial.print("Bus voltage: ");
  v = ina.readBusVoltage();
//    Serial.print(v, 3);
//    Serial.println(" V");
  arduino.print(v);
  arduino.print(", ");

//    Serial.print("Bus Power: ");
  i = ina.readBusPower();
//    Serial.print(i, 3);
//    Serial.println(" W");
  arduino.println(i);
}
