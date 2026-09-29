#include <stdio.h>
#include <omp.h>

int main() {
    int val = 10;
    int result[4] = {0};

    #pragma omp parallel for private(val) num_threads(4)
    for (int i = 0; i < 4; i++) {
        val += i; 
        result[i] = val;
    }

    printf("Original val: %d\n", val); 
    return 0;
}