// Implement a code using C language that reads a persons first and last name and displays a welcome message.

#include <stdio.h>

int main(void) {
    char name[50];

    // Prompt the user for input
    printf("Enter your name: ");

    scanf("%49s", name);
    printf("Hello, %s!\n", name);

}