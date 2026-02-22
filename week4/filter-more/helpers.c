#include "helpers.h"
#include <math.h>

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE *pixel = &image[i][j];
            int average = round((pixel->rgbtRed + pixel->rgbtGreen + pixel->rgbtBlue) / 3.0);
            pixel->rgbtRed = average;
            pixel->rgbtGreen = average;
            pixel->rgbtBlue = average;
        }
    }
}

void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
            copy[i][j] = image[i][j];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int total_red = 0, total_green = 0, total_blue = 0;
            int count = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        total_red += copy[ni][nj].rgbtRed;
                        total_green += copy[ni][nj].rgbtGreen;
                        total_blue += copy[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }

            image[i][j].rgbtRed = (int) round((float) total_red / count);
            image[i][j].rgbtGreen = (int) round((float) total_green / count);
            image[i][j].rgbtBlue = (int) round((float) total_blue / count);
        }
    }
}

void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};

    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
            copy[i][j] = image[i][j];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gx_red = 0, gy_red = 0;
            int gx_green = 0, gy_green = 0;
            int gx_blue = 0, gy_blue = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    if (ni < 0 || ni >= height || nj < 0 || nj >= width)
                        continue;

                    int kernel_i = di + 1;
                    int kernel_j = dj + 1;

                    gx_red += copy[ni][nj].rgbtRed * Gx[kernel_i][kernel_j];
                    gy_red += copy[ni][nj].rgbtRed * Gy[kernel_i][kernel_j];

                    gx_green += copy[ni][nj].rgbtGreen * Gx[kernel_i][kernel_j];
                    gy_green += copy[ni][nj].rgbtGreen * Gy[kernel_i][kernel_j];

                    gx_blue += copy[ni][nj].rgbtBlue * Gx[kernel_i][kernel_j];
                    gy_blue += copy[ni][nj].rgbtBlue * Gy[kernel_i][kernel_j];
                }
            }

            int red = (int) round(sqrt(gx_red * gx_red + gy_red * gy_red));
            int green = (int) round(sqrt(gx_green * gx_green + gy_green * gy_green));
            int blue = (int) round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));

            image[i][j].rgbtRed = red > 255 ? 255 : red;
            image[i][j].rgbtGreen = green > 255 ? 255 : green;
            image[i][j].rgbtBlue = blue > 255 ? 255 : blue;
        }
    }
}

