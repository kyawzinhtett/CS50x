#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    int length = strlen(input);

    // Base case
    if (length == 1)
    {
        return input[0] - '0';
    }

    // Convert last char to int
    int last_digit = input[length - 1] - '0';

    // Remove last char from string
    input[length - 1] = '\0';

    return last_digit + 10 * convert(input);
}