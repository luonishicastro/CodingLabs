// Implement a code using C language that reads a persons first and last name and displays a welcome message.

#include <stdio.h>
#include "cs50.h"

int main(void)
{
    string answer = get_string("Whats your name? ");
    printf("hello, %s \n", answer);
}