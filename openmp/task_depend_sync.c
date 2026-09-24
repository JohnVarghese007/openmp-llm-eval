#include <stdio.h>
#include <omp.h>

int main() {
    int x = 0;

    #pragma omp parallel
    {
        #pragma omp single
        {
        
            #pragma omp task depend(out: x)
            {
                x = 100;
            }

            
            #pragma omp task depend(in: x)
            {
                printf("Value of x: %d\n", x);
            }
        }
    }
    return 0;
}