#include <omp.h>
#include <stdio.h>

int main() {
    int flag = 0;

    #pragma omp parallel num_threads(4)
    {
        if (flag == 0) {
            flag = 1;
        }
    }

    printf("Flag = %d\n", flag);

    return 0;
}