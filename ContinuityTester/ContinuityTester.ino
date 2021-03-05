/* Short standalone script to for use in a small continuity checking board. 

  created:      21 Dec 2020
  by:           Ben Tait
  Last Edited:  23 Dec 2020
  by:           Ben Tait

*/


#define BTN_PIN 37

#define CH_NUM 3
// Pin Numbers for the GPIO Pins Used
int channels[CH_NUM] = {28, 30, 32}; 

int buttonStateOld = 0;
int buttonStateNew = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(BTN_PIN, INPUT);
  
}

void loop() {
  buttonStateOld = buttonStateNew;
  buttonStateNew = digitalRead(BTN_PIN);
  if (buttonStateNew == 1 && buttonStateOld == 0) {
    Serial.println("Beginning Continuity Test");

    for (int i = 0; i < CH_NUM; i++) {
      Serial.print("Testing Channel ");
      Serial.println(i);
      set_output(i);
      test_channel(i); 
    }
  }

}

// Sets the desired channels as an output and other channels as inputs
void set_output(int ch) {
  
  for (int i = 0; i < CH_NUM; i++) {
    if (i == ch) {
      pinMode(channels[i], OUTPUT);
    } else {
      pinMode(channels[i], INPUT);
    }
  }  
}

void test_channel(int ch) {
  int out = channels[ch];
  int in1 = channels[(ch + 2) % 3]; // "Left" of ch
  Serial.println(in1);
  int in2 = channels[(ch + 1) % 3]; // "Right" of ch
  Serial.println(in2);
  
  int res1, res2;

  digitalWrite(out, HIGH);
  res1 = digitalRead(in1);
  res2 = digitalRead(in2);

  delay(500);

  digitalWrite(out, LOW);
  
  Serial.print("Out1: ");
  Serial.print(res1);
  Serial.print(" Out2: ");
  Serial.println(res2);
}
