// Implement a code using C language that reads an employee's salary and shows their new salary with a 15% increase.

#include<stdio.h>

int main(void){
    float salario;
    float salarioAjustado;

    printf("Qual eh o salario do funcionaro em reais?");
    scanf("%f", &salario);

    salarioAjustado = salario * 0.15 + salario;

    printf("O novo salario do funcionario sera de: %.2f", salarioAjustado);
}