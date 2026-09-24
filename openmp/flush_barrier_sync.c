#include <stdio.h>
#include <omp.h>

int main() {
    int data = 0;
    int flag = 0;

    #pragma omp parallel num_threads(2)
    {
        int id = omp_get_thread_num();
        if (id == 0) {
            data = 42;
            #pragma omp flush(data, flag)
            flag = 1;
        }

        #pragma omp barrier

        if (id == 1) {
            printf("Flag: %d, Data: %d\n", flag, data);
        }
    }
    return 0;
}