// Implement a code using C language that reads an integer number and shows its successor and predecessor.

#include<stdio.h>

int main(void){
    int num;
    int numSuc;
    int numAnt;

    printf("Digite um numero qualquer: ");
    scanf("%d", &num);

    numSuc = num + 1;
    numAnt = num - 1;

    printf("Sucessor: %d\n", numSuc);
    printf("Antecessor: %d", numAnt);
}