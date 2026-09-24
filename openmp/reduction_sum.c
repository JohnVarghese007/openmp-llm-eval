#include <omp.h>
#include <stdio.h>

int main() {
    int sum = 0;
    int arr[100];

    for (int i = 0; i < 100; i++) {
        arr[i] = i + 1;
    }

    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < 100; i++) {
        sum += arr[i];
    }

    printf("%d\n", sum);

    return 0;
}