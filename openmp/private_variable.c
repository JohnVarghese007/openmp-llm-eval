#include <omp.h>
#include <stdio.h>

int main() {

    #pragma omp parallel
    {
        int local = omp_get_thread_num();

        printf("%d\n", local);
    }

    return 0;
}