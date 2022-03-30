
#include <stdlib.h>
#include <math.h>

#define DELTA_T 0.1
#define PROP_ACCELERATE 0.2
#define DISTURBANCE_MAGNITUDE 0.005
#define TERMINAL_VELOCITY -20
#define g -9.8
#define MASS 100 //kg
#define THRUST 3600 // kN

# define LENGTH 2000

int x=0, velocity=0, previous=0;

float thrust_accel = THRUST / MASS; 

int ledPin = 13;

float newtonian_kinematics(float x_0, float v, float a, float delta_t);

long t_0, previous_t;

void setup(){
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
    Serial.println("Set up Serial...");
    t_0 = millis();
}

int counter = 0;

int currLED = LOW;
void loop(){
    if(abs(millis() % 1000) < 10){
      currLED = (currLED == HIGH)? LOW : HIGH;
      digitalWrite(ledPin, currLED);
      Serial.println("toggle LED");
    }
    previous = x;
    if(counter < (LENGTH / DELTA_T)){
        x = newtonian_kinematics(previous, velocity, thrust_accel, DELTA_T); 
    } else {
        x = newtonian_kinematics(previous, velocity, g, DELTA_T);
    }
    velocity = (x - previous) / DELTA_T;
    Serial.println(x);
}

#define ALTITUDE_THRESHOLD 100 // m

float newtonian_kinematics(float x_0, float v, float a, float delta_t){
    float new_pos = x_0 + v * delta_t + (a * pow(delta_t,2))/2;
    float velocity = (new_pos - x_0) / delta_t;
    if (new_pos > ALTITUDE_THRESHOLD){
        int dir = (rand() % 2) * 2 - 1;
        float disturbance = DISTURBANCE_MAGNITUDE * dir * new_pos;
        new_pos += disturbance;
    }
    return new_pos;
}
