#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // pyramid rows
    for (int i = 0; i < height; i++)
    {
        // left-align space
        for (int j = height; j > i + 1; j--)
        {
            printf(" ");
        }

        // left-align pyramid column
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        
        printf("\n");
    }
}