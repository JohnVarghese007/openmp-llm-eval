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
            flag = 1; 
        } else if (id == 1) {
            while (flag == 0) {
                
            }
            printf("Flag: %d, Data: %d\n", flag, data);
        }
    }
    return 0;
}