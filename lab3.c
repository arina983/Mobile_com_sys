#include <stdio.h>

int main(){

    int x[5] = {0, 0, 0, 1, 1}; // 3
    int y[5] = {0, 1, 0, 1, 0}; //10
    int m = 5;
    int N = (1 << m) -1; // длина последовательности 2^5 - 1 = 31
    int gold[N];

    printf("x: ");
    for (int i = 0; i < m; i ++){
        printf("%d", x[i]);
    }
    printf("\n");
    printf("y: ");
    for (int i = 0; i < m; i ++){
        printf("%d", y[i]);
    }
    printf("\n");

    for (int i = 0; i < N; i ++){
        int out = x[4]^y[4]; // выход послдовательности 
        gold[i] = out;

        int XOR_x = x[3]^x[4]; // x4 XOR x5
        int XOR_y = y[1]^y[4]; // y2 XOR y5
    
        // сдвиг регистров
        for (int j = 4; j > 0; j--){
            x[j] = x[j-1];
            y[j] = y[j-1];
        }
        // запись новых битов в начало регистров
        x[0] = XOR_x;
        y[0] = XOR_y;
    }
    printf("Последовательность Голда:\n");
    for (int i = 0; i < N; i++){
        printf("%d", gold[i]);
        if ((i+1)%10 == 0){
            printf(" ");
        }
    }
    printf("\n");
    
    //2 циклический сдвиг последовательности и автокорреляция 
    printf("Сдвиг|");
    for (int b = 0; b < N; b++) printf("бит%-2d|",b+1);
    printf("Автокорр\n");
    printf("-----+");
    for (int b = 0; b < N; b++) printf("-----+");
    printf("--------\n");
    for (int k = 0; k < N; k++){
        int c = 0;
        int o = 0;
        printf("%5d|", k);
        
        for (int i = 0; i < N; i ++){
            int sdvig = gold[(i+k)%N];
            printf("   %d |", sdvig);
            if (gold[i] == sdvig)
                c++;
            else
                o++;
        }
        double R = (double)(c-o)/N;
        printf(" %+.4f\n", R); 
    }
    
    //3 x=x+1, а y= у-5.
    int x_3[5] = {0, 0, 1, 0, 0}; // 4
    int y_3[5] = {0, 0, 1, 0, 1}; // 5
    int gold_3[N];

    printf("x_3: ");
    for (int i = 0; i < m; i ++){
        printf("%d", x_3[i]);
    }
    printf("\n");
    printf("y_3: ");
    for (int i = 0; i < m; i ++){
        printf("%d", y_3[i]);
    }
    printf("\n");

    for (int i = 0; i < N; i ++){
        int out_3 = x_3[4]^y_3[4]; // выход послдовательности 
        gold_3[i] = out_3;

        int XOR_x_3 = x_3[3]^x_3[4]; // x4 XOR x5
        int XOR_y_3 = y_3[1]^y_3[4]; // y2 XOR y5
    
        // сдвиг регистров
        for (int j = 4; j > 0; j--){
            x_3[j] = x_3[j-1];
            y_3[j] = y_3[j-1];
        }
        // запись новых битов в начало регистров
        x_3[0] = XOR_x_3;
        y_3[0] = XOR_y_3;
    }
    printf("Последовательность Голда 2:\n");
    for (int i = 0; i < N; i++){
        printf("%d", gold_3[i]);
        if ((i+1)%10 == 0){
            printf(" ");
        }
    }
    printf("\n");

    //4 взаимная корреляция 
    int c = 0, o = 0;
    for (int i = 0; i < N; i ++){
        if (gold[i] == gold_3[i])
            c++;
        else 
            o++;
    }
    double R_3 = (double)(c - o) / N;
    printf("\nВзаимная корреляция: %+.4f\n", R_3);
    return 0;    
}