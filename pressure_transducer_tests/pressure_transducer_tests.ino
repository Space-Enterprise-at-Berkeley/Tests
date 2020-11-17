#include <math.h>
long time = millis();

//#define LOW_PRESSURE_LOX A2
#define LOW_PRESSURE_PROP A2
#define LOW_PRESSURE_INJECTOR A0

//#define HIGH_PRESSURE_PROP A4
//#define HIGH_PRESSURE_LOX A4

int input = 0;
bool shouldPrint = false;
void setup() {
  // put your setup code here, to run once:

  //pinMode(LOW_PRESSURE_LOX, INPUT);
  pinMode(LOW_PRESSURE_PROP, INPUT);
  pinMode(LOW_PRESSURE_INJECTOR, INPUT);
  //pinMode(HIGH_PRESSURE_PROP, INPUT);
  //pinMode(HIGH_PRESSURE_LOX, INPUT);

  Serial.begin(9600);
}

// 0.88V - 4.4V : ?? - 5000 PSI

int lowpressurelox, lowpressureprop, highpressurelox, highpressureprop, lowpressureinjector, highpressure;
int converted_lox_low, converted_prop_low, converted_lox_high, converted_prop_high, converted_inject_low, converted_high;

int periodic = 50;
void loop() {
  if (Serial.available() > 0)   {
    if(Serial.read() == '0'){
      shouldPrint = !shouldPrint;
    }
  }
  // put your main code here, to run repeatedly:
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
