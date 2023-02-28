#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BLOCK_SIZE 512
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open memory card
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("File could not be opend.\n");
        return 2;
    }

    BYTE buffer[BLOCK_SIZE];
    FILE *img;
    char filename[8];
    int count = 0;

    // Repeat until end of card:
    // Read 512 bytes into a buffer
    while (fread(buffer, BLOCK_SIZE, 1, file) == 1)
    {
        // If start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If not first JPEG
            if (count != 0)
            {
                fclose(img);
            }

            // If first JPEG
            sprintf(filename, "%03i.jpg", count++);
            // Open image file
            img = fopen(filename, "w");
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
        // If already found JPEG
        else if (count > 0)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }

    // Close any remaining files
    fclose(img);
    fclose(file);
}