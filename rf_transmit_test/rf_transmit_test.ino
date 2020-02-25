//to run on arduino nano.

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  Serial.println("Test");
}

int value = 0;
void loop() {
  // put your main code here, to run repeatedly:
  Serial.write(value);
  value++;
  delay(100);
}
