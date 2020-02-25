#define RFSERIAL Serial1
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  RFSERIAL.begin(57600);
  Serial.println("Ready to receive messages");
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(RFSERIAL.available()){
    Serial.println(RFSERIAL.read());
  }
}
