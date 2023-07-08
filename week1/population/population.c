#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int n;
    do
    {
        n = get_int("Start size: ");
    }
    while (n < 9);

    // TODO: Prompt for end size
    int e;
    do
    {
        e = get_int("End size: ");
    }
    while (e < n);

    // TODO: Calculate number of years until we reach threshold
    int i = 0;
    while (n < e)
    {
        n = n + (n / 3) - (n / 4);
        i++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", i);
}