#define PIN 4

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    int readVal = Serial.read();
    if(readVal == '1'){
      digitalWrite(PIN, HIGH);
      Serial.println("wrote output HIGH");
    } else if (readVal == '0'){
      digitalWrite(PIN, LOW);
      Serial.println("wrote output LOW");
    }
  }
}
