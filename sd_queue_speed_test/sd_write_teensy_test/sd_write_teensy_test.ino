#include <SPI.h>
#include <string>
#include <SdFat.h>
#include <TimeLib.h>

const int len = 10;
std::string testStrings[len] = {"this is a test 1", "this is the second test", "third test",
                          "{packet test, | }", "alsdkjfaoiweja;sdf", "alskdfjoweifjoas",
                          "9234823431566", "aksdjfowieuro", "o23i89soidfj2", "asjf0923jksdf"};
long startTime;
long currTime;

std::string str_file_name = "sd_speed_test_results.txt";
const char * file_name = str_file_name.c_str();

// SD_FAT_TYPE = 0 for SdFat/File as defined in SdFatConfig.h,
// 1 for FAT16/FAT32, 2 for exFAT, 3 for FAT16/FAT32 and exFAT.
#define SD_FAT_TYPE 0

#if SD_FAT_TYPE == 0
SdFat sd;
File file;
#elif SD_FAT_TYPE == 1
SdFat32 sd;
File32 file;
#elif SD_FAT_TYPE == 2
SdExFat sd;
ExFile file;
#elif SD_FAT_TYPE == 3
SdFs sd;
FsFile file;
#endif  // SD_FAT_TYPE

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
    temp->message = (char *)malloc(temp->length + 2);

    strncpy(temp->message, message.c_str(), temp->length + 1);
    temp->message[temp->length] = '\n'; // add \n to string when enqueue
    temp->message[temp->length + 1] = '\0';

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

  res = sd.begin(SdioConfig(FIFO_SDIO));
  Serial.print("sd builtin: ");
  Serial.println(res);

  Serial.print("filename: ");
  int i = 0;
  while(*(file_name +i) != '\0'){
    Serial.print(*(file_name + i));
    i++;
  }
  Serial.println();

  file.open(file_name, O_RDWR | O_CREAT);
  file.close();

  sdBuffer = newQueue();
}

int count = 0;

void loop() {
  Serial.print("top of loop ");
  Serial.println(count);


  startTime = micros();

  int numIterations = 1000;

  for (int j = 0; j < numIterations; j++) {
    write_to_SD(testStrings[j%len]);
  }

  currTime = micros();
  Serial.println("==== FINISHED ====");
  Serial.println("Did " + String(numIterations) + " writes in " + String(float(currTime - startTime)/ 1000 ) + " ms");
  Serial.println("For an average of " + String(float(currTime - startTime) / (numIterations)) + " us per write");
  Serial.println("\n\n");

  count++;
}


bool write_to_SD(std::string message) {
  // every reading that we get from sensors should be written to sd and saved.

    sdBuffer->enqueue(message);
    if(sdBuffer->length >= 40) {
      if(file.open(file_name, O_RDWR | O_APPEND)) {
        int initialLength = sdBuffer->length;
        for(int i = 0; i < initialLength; i++) {
          char *msg = sdBuffer->dequeue();
          file.write(msg);
          free(msg);
        }
        file.close();
        return true;
      }
      else {                                                            //If the file didn't open
        return false;
      }
    }
}
