#include <omp.h>

int main() {
    int arr[100];

    arr[0] = 1;

    #pragma omp parallel for
    for (int i = 1; i < 100; i++) {
        arr[i] = arr[i - 1] + 1;
    }

    return 0;
}