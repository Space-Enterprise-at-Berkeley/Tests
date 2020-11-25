#include <iostream>
#include <cstring>
#include <chrono>
#include <ctime>
#include <ratio>

using namespace std;

struct Queue {

  struct Node {
    struct Node *next;
    char *message;
    int length; //length doesn't include the null terminator
  };

  uint16_t length = 0;

  struct Node *end = 0;
  struct Node *front = 0;

  void enqueue(string message) {
    struct Node *temp;
    length++;
    temp = (struct Node *)malloc(sizeof(struct Node));
    temp->length = message.length();
    temp->message = (char *)malloc(temp->length + 1);

    strncpy(temp->message, message.c_str(), temp->length + 1);
//    int i = 0;
//    while(*(temp->message +i) != '\0') {
//      Serial.print(*(temp->message + i));
//      i++;
//    }

    temp->next = nullptr;
    if (!front) {
      front = temp;
    } else {
      end->next = temp;
    }
    end = temp;
  }

  char * dequeue() { // string still needs to be cleared after dequeue; be very careful about this; wherever this is called.
    //cout << "length: " << +length << endl;
    if(length > 0) {
      length--;
      struct Node *tmp = front;
      char *msg = tmp->message;

      //strncpy(buf, tmp->message, tmp->length + 1);
//      int i = 0;
//      while(*(msg +i) != '\0'){
//        Serial.print(*(msg + i));
//        i++;
//      }

      if( length != 0){
        front = front->next;
      } else {
        front = nullptr;
        end = nullptr;
      }
      //free(tmp->message);
      tmp->message = nullptr;
      tmp->next = nullptr;
      free(tmp);
      int i = 0;
      // while(*(msg + i) != '\0'){
      //   cout << *(msg + i);
      //   i++;
      // }
      // cout << endl;
      free(msg);
      return nullptr;
    }
    return NULL;
  }
};

struct Queue * newQueue() {
  struct Queue *q = (struct Queue *)malloc(sizeof(struct Queue));
  q->length = 0;
  q->front=nullptr;
  q->end=nullptr;
  return q;
}

void freeAllQueueResources(struct Queue * q){
  if(!q->front)
    free(q->front);
  if(!q->end)
    free(q->end);
  free(q);
}


const int len = 10;
string testStrings[len] = {"this is a test 1", "this is the second test", "third test",
                          "{packet test, | }", "alsdkjfaoiweja;sdf", "alskdfjoweifjoas",
                          "9234823431566", "aksdjfowieuro", "o23i89soidfj2", "asjf0923jksdf"};

struct Queue *sdBuffer;

int main(int argc, char **argv) {

  int iterationCount = 0;
  sdBuffer = newQueue();

  while(true) {


    auto startTime = chrono::high_resolution_clock::now();

    int numIterations = 10000000;

    for (int j = 0; j < numIterations; j++) {
      sdBuffer->enqueue(testStrings[j%len]);
      if(j % 2 == 0) {
        char *msg = sdBuffer->dequeue();
        free(msg);
      }
      if(j % 100 == 0) {
        //while (sdBuffer->length > 0) {
          char *msg = sdBuffer->dequeue();
          free(msg);
        //}
      }
    }
    cout << "finished combined enqueue, dequeue\n";

    //
    // for (int j = 0; j < numIterations; j++) {
    //   sdBuffer->enqueue(testStrings[j%len]);
    // }
    // cout << "finished enqueue\n";
    //
    while (sdBuffer->length > 0) {
      char *dequeuedMsg = sdBuffer->dequeue();
      // int j = 0;
      // while (*(dequeuedMsg + j) != '\0'){
      //   cout << *(dequeuedMsg + j);
      //   j++;
      // }
      // cout << endl;
      free(dequeuedMsg);
    }
    cout << "Finished dequeue\n";

    auto timeElapsed = chrono::high_resolution_clock::now() - startTime;
    long timeElapsedNanos = chrono::duration_cast<chrono::nanoseconds>(timeElapsed).count();
    cout << "==== FINISHED ====\n";
    cout << "Did " << numIterations << " writes in " << timeElapsedNanos << " ns\n";
    cout << "For an average of " << timeElapsedNanos / (numIterations) << " ns per write\n\n\n";

    //freeAllQueueResources(sdBuffer);
    iterationCount++;
  }
}
