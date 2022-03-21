#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <pthread.h>
#include <unistd.h>
#include <math.h>
#include <stdbool.h>

#define CALCULATION_START 9999999999999999

bool is_prime(long long number) {
  assert(number >= 0);
  if (number == 0 || number == 1) return true;
  for (long long i = 2; i <= sqrt(number); i++) {
      if (number % i == 0) {
          return false;
      }
    }
    return true;
}

void *perform_work(void *arguments){
  int index = *((int *)arguments);
  printf("THREAD %d: Started.\n", index);
  while (true) {
    for (long long i = CALCULATION_START;; i++) {
      if (is_prime(i)) {
        printf("THREAD %d found new prime number %lld\n", index, i);
      }
    }
  }
  printf("THREAD %d: Ended.\n", index);
  return NULL;
}

// void *perform_work(void *arguments){
//   int index = *((int *)arguments);
//   int lifetime = rand() % 5 + 5;
//   int seconds_passed = 0;
//   printf("THREAD %d: Started.\n", index);
//   while (seconds_passed <= lifetime) {
//     seconds_passed++;
//     for (long long i = CALCULATION_START;; i++) {
//       if (is_prime(i)) {
//         printf("THREAD %d found new prime number %lld\n", index, i);
//       }
//     }
//   }
//   printf("THREAD %d: Ended.\n", index);
//   return NULL;
// }

int main(int argc, char** argv) {
  assert(argc == 2);
  int number_of_threads = atoi(argv[1]);
  printf("Number of threads: %d\n", number_of_threads);

  pthread_t* threads = (pthread_t*) calloc(number_of_threads, sizeof(pthread_t));
  int* thread_args = (int*) calloc(number_of_threads, sizeof(int));
  int* thread_lifetimes = (int*) calloc(number_of_threads, sizeof(int));

  if (threads == NULL || thread_args == NULL) {
    printf("Memory not allocated.\n");
    exit(0);
  }

  int i, result_code;
  
  for (int i = 0; i < number_of_threads; i++) {
    thread_lifetimes[i] = rand() % 5 + 5;
  }

  //create all threads one by one
  for (i = 0; i < number_of_threads; i++) {
    printf("IN MAIN: Creating thread %d.\n", i);
    thread_args[i] = i;
    result_code = pthread_create(&threads[i], NULL, perform_work, &thread_args[i]);
    assert(!result_code);
  }

  printf("IN MAIN: All threads are created.\n");

  int killed_threads_counter = 0;
  int seconds = 0;
  while(killed_threads_counter < number_of_threads) {
    sleep(1);
    seconds++;
    for (int i = 0; i < number_of_threads; i++) {
      if (thread_lifetimes[i] <= seconds && thread_lifetimes[i] != 0) {
        killed_threads_counter++;
        thread_lifetimes[i] = 0;
        result_code = pthread_cancel(threads[i]);
        assert(!result_code);
        printf("IN MAIN: Thread %d has ended.\n", i);
      }
    }
  }

  free(threads);
  free(thread_args);
  free(thread_lifetimes);

  printf("MAIN program has ended.\n");
  return 0;
}