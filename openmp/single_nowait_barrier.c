#include <stdio.h>
#include <omp.h>

int main() {
    int shared_var = 0;

    #pragma omp parallel num_threads(2)
    {
        #pragma omp single nowait
        {
            shared_var = 99;
        }

        
        #pragma omp barrier

        if (omp_get_thread_num() == 1) {
            printf("Shared var: %d\n", shared_var);
        }
    }
    return 0;
}