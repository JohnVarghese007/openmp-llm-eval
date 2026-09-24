#include <omp.h>
#include <stdio.h>

int main() {
    int value = 0;

    #pragma omp parallel num_threads(2)
    {
        if (omp_get_thread_num() == 0) {
            value = 42;
        }

        #pragma omp barrier

        printf("%d\n", value);
    }

    return 0;
}