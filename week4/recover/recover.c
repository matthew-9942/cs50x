#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover card\n");
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("Could not open the file.\n");
        return 1;
    }

    uint8_t buffer[512];
    FILE *img = NULL;
    int count = 0;
    char filename[8];

    while (fread(buffer, 512, 1, f) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            count++;
        }
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), 512, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }
    fclose(f);
    return 0;
}

