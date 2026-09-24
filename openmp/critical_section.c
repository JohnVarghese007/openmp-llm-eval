#include <omp.h>
#include <stdio.h>

int main() {
    int counter = 0;

    #pragma omp parallel for
    for (int i = 0; i < 1000; i++) {

        #pragma omp critical
        {
            counter++;
        }

    }

    printf("%d\n", counter);

    return 0;
}