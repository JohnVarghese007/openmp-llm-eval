#include <omp.h>

int main() {
    int arr[10] = {0};

    #pragma omp parallel for
    for (int i = 0; i < 1000; i++) {
        arr[0]++;
    }

    return 0;
}
