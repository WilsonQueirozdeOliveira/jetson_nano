#include <stdio.h>
#include <pthread.h>

int counter1 = 0, counter2 = 0;

void* threadFunction1(void* arg) {
    int i;
    for (i = 0; i < 1000000; i++) {
        counter1++;
    }
    pthread_exit(NULL);
}

void* threadFunction2(void* arg) {
    int i;
    for (i = 0; i < 1000000; i++) {
        counter2++;
    }
    pthread_exit(NULL);
}

int main() {
    pthread_t thread_id1, thread_id2;

    pthread_create(&thread_id1, NULL, threadFunction1, NULL);
    pthread_create(&thread_id2, NULL, threadFunction2, NULL);

    pthread_join(thread_id1, NULL);
    pthread_join(thread_id2, NULL);

    printf("Counter1 = %d, Counter2 = %d\n", counter1, counter2);

    return 0;
}
