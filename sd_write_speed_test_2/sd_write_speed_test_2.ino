#include <SD.h>
#include <SPI.h>


const int len = 10;
String testStrings[len] = {"this is a test 1", "this is the second test", "third test",
                          "{packet test, | }", "alsdkjfaoiweja;sdf", "alskdfjoweifjoas",
                          "9234823431566", "aksdjfowieuro", "o23i89soidfj2", "asjf0923jksdf"};
long startTime;
long currTime;

char * file_name = String("sd_speed_test_results.txt").c_str();

void setup() {
  // put your setup code here, to run once:
  SD.begin(BUILTIN_SDCARD);
  startTime = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  int numIterations = 1000000000;
  for (int i = 0; i < numIterations; i++){
    write_to_SD(testStrings[i%len]);
  }
  currTime = millis();
  Serial.println("==== FINISHED ====");
  Serial.println("Did " + String(numIterations) + " writes in " + String((currTime - startTime)/ 1000 ) + "seconds");
  Serial.println("For an average of " + String((currTime - startTime) / (numIterations)) + " ms per write");
}


struct Queue {

  struct Node {
    struct Node* next;
    const char* message;
    int length;
  };
  
  uint8_t length = 0;
  
  struct Node *front = NULL;
  struct Node *end = NULL;
  
  void enqueue(String message) {
    struct Node *temp;
    length++;
    temp = (struct Node *)malloc(sizeof(struct Node));
    temp->length = message.length();
    temp->message = (char *)malloc(temp->length + 1);
    temp->message = message.c_str();
    temp->next = NULL;
    if (front == NULL) {
      front = temp;
    } else {
      end->next = temp;
    }
    end = temp;
  }
  
  const char *dequeue() { // string still needs to be cleared after dequeue; be very careful about this; wherever this is called.
    if(length > 0){
      length--;
      Node *tmp = front;
      const char *msg = tmp->message;
      front = front->next;
      free(tmp);
      return msg;
    } else {
      return NULL;
    }
  }
};

struct Queue *sdBuffer = (struct Queue *)malloc(sizeof(struct Queue));
File myFile;

bool write_to_SD(String message) {
  // every reading that we get from sensors should be written to sd and saved.

    sdBuffer->enqueue(message);

    if(sdBuffer->length == 20) {
      myFile = SD.open(file_name, O_CREAT | O_WRITE);
      if(myFile) {                                                      //If the file opened
        for(int i = 0; i <= sdBuffer->length; i++){
          const char *msg = sdBuffer->dequeue();
          //strcpy_P(buffer, (char *)pgm_read_word(&(packet_table[i])));  // Necessary casts and dereferencing, just copy.
          myFile.println(msg);
        }
        myFile.close();
        return true;
      }
      else {                                                            //If the file didn't open
        return false;
      }
    }
}
