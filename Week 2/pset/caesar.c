#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    // Make sure every character in argv[1] is a digit
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert argv[1] from a `string` to an `int`
    int k = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // For each character in the plaintext:
    int length = strlen(plaintext);
    char ciphertext[length];

    for (int i = 0; i < length; i++)
    {
        // Rotate the character if it's a letter
        ciphertext[i] = rotate(plaintext[i], k);
    }

    ciphertext[length] = '\0';

    printf("ciphertext: %s\n", ciphertext);
}

// Check the Key
bool only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }

    return true;
}

char rotate(char c, int n)
{
    if (isupper(c))
    {
        c -= 65;
        c = (c + n) % 26;
        c += 65;
    }

    if (islower(c))
    {
        c -= 97;
        c = (c + n) % 26;
        c += 97;
    }

    return c;
}