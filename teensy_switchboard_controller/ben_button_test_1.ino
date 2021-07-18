#include <keyboard.h>
#include <Bounce.h>
//Pin layout here
const int buttonPin = 1; //connect the button to pin 1
Bounce pushButton = Bounce(buttonPin, 10);
const int buttonPin2 = 4; //connect the button to pin 4
Bounce pushButton2 = Bounce(buttonPin2, 10);
const int buttonPin3 = 6;
Bounce pushButton3 = Bounce(buttonPin3, 10);
const int buttonPin4 = 9;
Bounce pushButton4 = Bounce(buttonPin4, 10);
int buttonState = 0;
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;

void setup(){
    pinMode(buttonPin, INPUT_PULLUP);
    Serial.begin(57600);
    pinMode(buttonPin2, INPUT_PULLUP);
    pinMode(buttonPin3, INPUT_PULLUP);
    pinMode(buttonPin4, INPUT_PULLUP);
}
void loop(){
  buttonState = digitalRead(buttonPin);
  byte previousState = HIGH; // what state was the button last time
  unsigned int count =0;  // how many times has it changed to low
  unsigned long countAt = 0; // when count changed
  unsigned int countPrinted = 0; // last count printed
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  buttonState4 = digitalRead(buttonPin4);
  //replace key Z with your desired key
  if (pushButton.update()){
    if (pushButton.fallingEdge()) {
        count = count +1;
        Keyboard.set_key1(KEY_8);
        Keyboard.set_key2(KEYPAD_ASTERIX);
        Keyboard.send_now();
        Keyboard.set_key1(0);
        Keyboard.set_key2(0);
        Keyboard.send_now();
        countAt = millis();
    } else if (pushButton.risingEdge()) {
         Keyboard.set_key1(0);
         Keyboard.set_key2(0);
         Keyboard.send_now();
      }
   } else if (pushButton2.update()){
    if (pushButton2.fallingEdge()) {
        count = count +1;
        Keyboard.set_key1(KEY_2);
        Keyboard.set_key2(KEY_PERIOD);
        Keyboard.send_now();
        Keyboard.set_key1(0);
        Keyboard.set_key2(0);
        Keyboard.send_now();
        countAt = millis();
    } else if (pushButton2.risingEdge()) {
         Keyboard.set_key1(0);
         Keyboard.set_key2(0);
         Keyboard.send_now();
      }
   
   }else {
    if (count != countPrinted) {
      unsigned long nowMillis = millis();
      if (nowMillis - countAt > 100) {
        Serial.print("count: ");
        Serial.println(count);
        countPrinted = count;
      }
    }
   }
  }
