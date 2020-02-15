
#define PARACHUTE_OUTPUT 3
#define ALTITUDE_INPUT 5

void setup(){
    pinMode(PARACHUTE_OUTPUT, OUTPUT);
    pinMode(ALTITUDE_INPUT, INPUT);    
}

#define LENGTH 30
float buffer[LENGTH];
int index = 0;
void loop(){
    buffer[index] = digitalRead(ALTITUDE_INPUT);
    index++;
    index %= LENGTH;
    if (atApogee(buffer, index)){
        digitalWrite(PARACHUTE_OUPUT, HIGH);
    }
}

bool atApogee(float *altitude, index){
    int i_1 = (index - 1) % LENGTH;
    int i_2 = (index - 2) % LENGTH;
    int i_3 = (index - 3) % LENGTH;
    return (altitude[index] < altitude[i_1]) && (altitude[i_1] < altitude[i_2]) && (altitude[i_2] < altitude[i_3]);
}
