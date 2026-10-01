#include <stdio.h>
#include <math.h>
#include <omp.h>

#define N 64
#define STEPS 10

double A[N][N];
double A_new[N][N];

void init_grid() {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (i == 0 || i == N - 1 || j == 0 || j == N - 1) {
                A[i][j] = 100.0;
                A_new[i][j] = 100.0;
            } else {
                A[i][j] = 0.0;
                A_new[i][j] = 0.0;
            }
        }
    }
}

int main() {
    init_grid();

    for (int iter = 0; iter < STEPS; iter++) {
        #pragma omp parallel for
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                A_new[i][j] = 0.25 * (A[i - 1][j] + A[i + 1][j] + A[i][j - 1] + A[i][j + 1]);
            }
        }

        #pragma omp parallel for collapse(3)
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                A[i][j] = A_new[i][j];
            }
        }
    }

    printf("Jacobi stencil completed. Center value: %f\n", A[N / 2][N / 2]);
    return 0;
}