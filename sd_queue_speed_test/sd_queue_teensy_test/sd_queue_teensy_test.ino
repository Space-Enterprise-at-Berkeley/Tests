#include <SD.h>
#include <SPI.h>
#include <string>

const int len = 10;
std::string testStrings[len] = {"this is a test 1", "this is the second test", "third test",
                          "{packet test, | }", "alsdkjfaoiweja;sdf", "alskdfjoweifjoas",
                          "9234823431566", "aksdjfowieuro", "o23i89soidfj2", "asjf0923jksdf"};
long startTime;
long currTime;

const char * file_name = String("sd_speed_test_results.txt").c_str();


struct Queue {

  struct Node {
    struct Node *next;
    char *message;
    int length; //length doesn't include the null terminator
  };

  uint16_t length = 0;

  struct Node *end = 0;
  struct Node *front = 0;

  void enqueue(std::string message) {
    struct Node *temp;
    length++;
    temp = (struct Node *)malloc(sizeof(struct Node));

    temp->length = message.length();
    temp->message = (char *)malloc(temp->length + 1);

    strncpy(temp->message, message.c_str(), temp->length + 1);

    temp->next = nullptr;
    if (!front) {
      front = temp;
    } else {
      end->next = temp;
    }
    end = temp;
  }

  char * dequeue() { // string still needs to be cleared after dequeue; be very careful about this; wherever this is called.
    if(length > 0) {
      length--;
      struct Node *tmp = front;
      char *msg = tmp->message;

      if(length != 0) {
        front = tmp->next;
      } else {
        front = nullptr;
        end = nullptr;
      }

      tmp->message = nullptr;
      tmp->next = nullptr;
      free(tmp);

      return msg;
    }
    return nullptr;
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
  sdBuffer = newQueue();
}

int count = 0;
void loop() {
  Serial.print("top of loop ");
  Serial.println(count);


  startTime = micros();

  int numIterations = 10000;

  for (int j = 0; j < numIterations; j++) {
    sdBuffer->enqueue(testStrings[j%len]);
  }
  Serial.println("finished enqueue");

  Serial.flush();
  for (int i = 0; i < numIterations; i++){
    char *dequeuedMsg = sdBuffer->dequeue();
    free(dequeuedMsg);
  }
  Serial.println("Finished dequeue");

  currTime = micros();
  Serial.println("==== FINISHED ====");
  Serial.println("Did " + String(numIterations) + " writes in " + String(float(currTime - startTime)/ 1000 ) + " ms");
  Serial.println("For an average of " + String(float(currTime - startTime) / (numIterations)) + " us per write");
  Serial.println("\n\n");

  count++;
}

File myFile;

bool write_to_SD(std::string message) {
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
