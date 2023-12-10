// Implement a code using C language that reads two grades of a student, calculates, and displays their average.

#include<stdio.h>

int main(void){
    float nota1;
    float nota2;
    float mediaNotas;

    printf("Qual a primeira nota do Aluno? ");
    scanf("%f", &nota1);
    printf("Qual a segunda nota do Aluno? ");
    scanf("%f", &nota2);

    mediaNotas = (nota1 + nota2) / 2;

    printf("A media entre as notas foi: %.2f", mediaNotas);
}