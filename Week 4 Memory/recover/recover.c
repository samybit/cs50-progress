#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check for correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open forensic image
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Buffer for 512-byte blocks
    uint8_t buffer[512];

    FILE *img = NULL;
    int file_count = 0;
    char filename[8]; // "###.jpg\0"

    // Read until end of card
    while (fread(buffer, sizeof(uint8_t), 512, card) == 512)
    {
        // Check for JPEG header
        bool is_jpeg = (buffer[0] == 0xff) &&
                       (buffer[1] == 0xd8) &&
                       (buffer[2] == 0xff) &&
                       ((buffer[3] & 0xf0) == 0xe0);

        if (is_jpeg)
        {
            // If already writing a file, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // Open new JPEG file
            snprintf(filename, sizeof(filename), "%03d.jpg", file_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                // Clean up and exit on error
                fclose(card);
                return 1;
            }
            file_count++;
        }

        // If currently writing a JPEG, write this block
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), 512, img);
        }
    }

    // Close any open files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);

    return 0;
}
