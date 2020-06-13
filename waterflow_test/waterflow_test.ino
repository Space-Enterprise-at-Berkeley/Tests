#include <math.h>
long time = millis();

#define LOW_PRESSURE_1 A0
#define LOW_PRESSURE_2 A1
#define LOW_PRESSURE_3 A2
#define LOW_PRESSURE_4 A3

#define HIGH_PRESSURE_1 A4
#define HIGH_PRESSURE_2 A5

int input = 0;
bool shouldPrint = false;

int numLowPressure = 0;
int numHighPressure = 0;

void setup() {
  Serial.begin(9600);

  Serial.println("How many low pressure sensors are connected?");
  while (!Serial.available());
  
  int lowPressureRead = Serial.read();
  numLowPressure = lowPressureRead - 48;
  
  Serial.println("How many low pressure sensors are connected?");
  while (!Serial.available());

  numHighPressure = Serial.read() - 48;

  pinMode(LOW_PRESSURE_1, INPUT);
  pinMode(LOW_PRESSURE_2, INPUT);
  pinMode(LOW_PRESSURE_3, INPUT);
  pinMode(LOW_PRESSURE_4, INPUT);
  
  pinMode(HIGH_PRESSURE_1, INPUT);
  pinMode(HIGH_PRESSURE_2, INPUT);

}

// 0.88V - 4.4V : ?? - 5000 PSI

int lowpressurelox, lowpressureprop, highpressurelox, highpressureprop, lowpressureinjector, highpressure;
int converted_lox_low, converted_prop_low, converted_lox_high, converted_prop_high, converted_inject_low, converted_high;

int periodic = 50;
void loop() {
  if (Serial.available() > 0)   {
    int readByte = Serial.read();
    if(readByte == 't'){
      shouldPrint = true;
    } else if(readByte == 'f'){
      shouldPrint = false;
    } else if(readByte == '0'){
      shouldPrint = !shouldPrint;
    }
  }
  
  //lowpressurelox = analogRead(LOW_PRESSURE_LOX);
  lowpressureprop = analogRead(LOW_PRESSURE_PROP);
  lowpressureinjector = analogRead(LOW_PRESSURE_INJECTOR);
  //highpressureprop = analogRead(HIGH_PRESSURE_PROP);
  //highpressure = analogRead(HIGH_PRESSURE_PROP);
  

  //converted_lox_low = lowPressureConversion(lowpressurelox);
  converted_prop_low = lowPressureConversion(lowpressureprop);
  converted_inject_low = lowPressureConversion(lowpressureinjector);

  //converted_high = highPressureConversion(highpressure);
  //converted_prop_high= highPressureConversion(highpressureprop);

  char buffer[25];
 
  time = millis();
  if((time%int(periodic)) == 0){
//  sprintf(buffer, "%d,%d,%d,%d,%d", lowpressurelox, lowpressureprop, highpressurelox, highpressureprop, lowpressureinjector);
//  sprintf(buffer, "%d,%d,%d,%d,%d", converted_lox_low, converted_prop_low, converted_high_lox, converted_high_prop, converted_inject_low);
    //String toWriteRaw = String(lowpressurelox)+','+String(lowpressureprop)+','+String(highpressure);
    String toWrite = String(converted_inject_low)+','+String(converted_prop_low); // +','+String(converted_prop_high); //+','+String(converted_high_prop);
    //if(converted_lox_low > 10 || converted_prop_low > 10  || converted_high_prop > 40){
    if(shouldPrint){
      Serial.println(toWrite);
    }
    //}
  }
}

int _lowPressureConversion(int raw){
  return (raw - 123);
}

int _highPressureConversion(int raw){
  return (6*raw - 1237);
}

float lowPressureConversion(int raw){
  return int(1.2258857538273733*raw - 123.89876445934394);
}

float highPressureConversion(int raw){
  return (6.612739309669555*(raw - 0.88 / 4.4 * 1024)); //- 1237.7612969223858);
}
