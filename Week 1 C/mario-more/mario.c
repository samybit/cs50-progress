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

    for (int i = 0; i < height; i++)
    {
        // for left spaces
        for (int s = 0; s < height - i - 1; s++)
        {
            printf(" ");
        }

        // for left # side
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // for gap of 2 spaces
        printf("  ");

        // for right # side
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}
