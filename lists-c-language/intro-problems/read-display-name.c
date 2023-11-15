// Implement a code using C language that reads a persons first and last name and displays a welcome message.

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string first = get_string("Whats your first name? ");
    string last = get_string("Whats your last name? ");
    printf("hello, %s %s\n", first, last);
}