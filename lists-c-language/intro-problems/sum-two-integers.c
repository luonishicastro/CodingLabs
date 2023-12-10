// Implement a code using C language that reads two numbers and display the sum of them.

#include<stdio.h>

int main(void){
    int num1;
    int num2;
    int num3;

    printf("Digite um numero qualquer: ");
    scanf("%d", &num1);
    printf("Digite mais um numero qualquer: ");
    scanf("%d", &num2);

    num3 = num2 + num1;

    printf("O resultado final foi de: %d", num3);
}