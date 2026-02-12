#include <stdio.h>

int is_alphabetical(char letter);
int is_blank(char letter);
int is_punctuation(char letter);

int main(void)
{
    char text[1024];
    printf("Text: ");
    fgets(text, 1024, stdin);
    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0; text[i] != '\0'; i++)
    {
        letters += is_alphabetical(text[i]) ? 1 : 0;
        words += is_blank(text[i]);
        sentences += is_punctuation(text[i]);
    }

    float average_letters = ((float) letters / words) * 100;
    float average_sentences = ((float) sentences / words) * 100;
    int index = (0.0588 * average_letters - 0.296 * average_sentences - 15.8) + 0.5;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

    return 0;
}

int is_alphabetical(char letter)
{
    return ((letter >= 'a' && letter <= 'z') || (letter >= 'A' && letter <= 'Z')) ? 1 : 0;
}

int is_blank(char letter)
{
    return (letter == ' ') ? 1 : 0;
}

int is_punctuation(char letter)
{
    return (letter == '.' || letter == '?' || letter == '!') ? 1 : 0;
}

