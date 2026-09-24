#include <omp.h>
#include <stdio.h>

int main() {
    int a = 0;
    int b = 0;

    #pragma omp parallel sections
    {
        #pragma omp section
        {
            a = 42;
        }

        #pragma omp section
        {
            b = a;
        }
    }

    printf("%d %d\n", a, b);

    return 0;
}