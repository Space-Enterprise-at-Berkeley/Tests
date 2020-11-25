#include <SD.h>
#include <SPI.h>


const int len = 10;
String testStrings[len] = {F("this is a test 1"), F("this is the second test"), F("third test"),
                          F("{packet test, | }"), F("alsdkjfaoiweja;sdf"), F("alskdfjoweifjoas"),
                          F("9234823431566"), F("aksdjfowieuro"), F("o23i89soidfj2"), F("asjf0923jksdf")};
long startTime;
long currTime;

const char * file_name = String("sd_speed_test_results.txt").c_str();

#ifdef __arm__
// should use uinstd.h to define sbrk but Due causes a conflict
extern "C" char* sbrk(int incr);
#else  // __ARM__
extern char *__brkval;
#endif  // __arm__

int freeMemory() {
  char top;
#ifdef __arm__
  return &top - reinterpret_cast<char*>(sbrk(0));
#elif defined(CORE_TEENSY) || (ARDUINO > 103 && ARDUINO != 151)
  return &top - __brkval;
#else  // __arm__
  return __brkval ? &top - __brkval : &top - __malloc_heap_start;
#endif  // __arm__
}

struct Queue {

  struct Node {
    struct Node *next;
    char *message;
    int length; //length doesn't include the null terminator
  };
  
  uint8_t length = 0;

  struct Node *end = 0;
  struct Node *front = 0;
  
  void enqueue(String message) {
    struct Node *temp;
    length++;
//    Serial.print("incremented length to: ");
//    Serial.println(length);
//    Serial.flush();
    temp = (struct Node *)malloc(sizeof(struct Node));
//    Serial.println("malloced");
//    Serial.flush();
    temp->length = message.length();
//    Serial.println("set length of node");
//    Serial.flush();
    temp->message = (char *)malloc(temp->length + 1);
//    Serial.println("malloced space for char array");
//    Serial.flush();
    strncpy(temp->message, message.c_str(), temp->length + 1);
//    Serial.print("in enqueue: ");
//    int i = 0;
//    while(*(temp->message +i) != '\0') {
//      Serial.print(*(temp->message + i));
//      i++;
//    }
//    Serial.println();
//    Serial.println("assigned char array");
//    Serial.flush();
    temp->next = 0;
//    Serial.println("Assigned next to NULL");
//    Serial.flush();
//    Serial.println((int)front);
//    Serial.println((int)end);
//    Serial.flush();
    if (!front) {
//      Serial.println("front is null; assigning to front");
//      Serial.flush();
      front = temp;
    } else {
//      Serial.println("front not null; extending end");
//      Serial.flush();
      end->next = temp;
    }
//    Serial.println("assigned node pointer right place");
//    Serial.flush();
    end = temp;
//    Serial.println("done, exiting");
//    Serial.flush();
  }
  
  char *dequeue() { // string still needs to be cleared after dequeue; be very careful about this; wherever this is called.
    if(length > 0) {
      length--;
      struct Node *tmp = front;
      char *msg = tmp->message;
//      int i = 0;
//      while(*(msg +i) != '\0'){
//        Serial.print(*(msg + i));
//        i++;
//      }
//      Serial.println();
//      Serial.flush();
      front = front->next;
      free(tmp);
      return msg;
    } else {
      return NULL;
    }
  }
};


struct Queue * newQueue() {
  struct Queue *q = (struct Queue *)malloc(sizeof(struct Queue));
  q->length = 0;
  q->front=nullptr;
  q->end=nullptr;
  return q;
}

struct Queue *sdBuffer;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  Serial.println("started up");
  int res;
  res = SD.begin(BUILTIN_SDCARD);
  Serial.println(res);
  int i = 0;
  while(*(file_name +i) != '\0'){
    Serial.print(*(file_name + i));
    i++;
  }
  Serial.println();
  Serial.print("free mem: ");
  Serial.println(freeMemory());

  int * test = (int *)malloc(10 * 4096 * sizeof(int));
  delay(100);
  Serial.print("free mem: ");
  Serial.println(freeMemory());
  free(test);
  delay(100);
  Serial.print("free mem: ");
  Serial.println(freeMemory());
}

int count = 0;
void loop() {
  Serial.print("top of loop ");
  Serial.println(count);

  sdBuffer = newQueue();  

  startTime = micros();

  int numIterations = 10000;
  Serial.print("free memory: ");
  Serial.println(freeMemory());
  for (int j = 0; j < numIterations; j++) {
    sdBuffer->enqueue(testStrings[j%len]);
//    Serial.print("free memory: ");
//    Serial.println(freeMemory());
  }
  Serial.println("finished enqueue");
  Serial.print("free memory: ");
  Serial.println(freeMemory());
  Serial.flush();
  for (int i = 0; i < numIterations; i++){
    char *dequeuedMsg = sdBuffer->dequeue();
    free(dequeuedMsg);
//    Serial.print("free memory: ");
//    Serial.println(freeMemory());
  }
  Serial.println("Finished dequeue");
  Serial.print("free memory: ");
  Serial.println(freeMemory());
  
  currTime = micros();  
  Serial.println("==== FINISHED ====");
  Serial.println("Did " + String(numIterations) + " writes in " + String(float(currTime - startTime)/ 1000 ) + " ms");
  Serial.println("For an average of " + String(float(currTime - startTime) / (numIterations)) + " us per write");
  Serial.println("\n\n");

  free(sdBuffer);
  count++;
}

////File myFile;
//
//bool write_to_SD(String message) {
//  // every reading that we get from sensors should be written to sd and saved.
//
//    sdBuffer->enqueue(message);
//
//    if(sdBuffer->length == 20) {
//      myFile = SD.open(file_name, O_CREAT | O_WRITE);
//      if(myFile) {                                                      //If the file opened
//        for(int i = 0; i <= sdBuffer->length; i++){
//          const char *msg = sdBuffer->dequeue();
//          //strcpy_P(buffer, (char *)pgm_read_word(&(packet_table[i])));  // Necessary casts and dereferencing, just copy.
//          myFile.println(msg);
//        }
//        myFile.close();
//        return true;
//      }
//      else {                                                            //If the file didn't open
//        return false;
//      }
//    }
//}
