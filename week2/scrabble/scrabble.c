#include <stdio.h>

int get_score(char *word);

int alphabet[26][2] = {{'A', 1}, {'B', 3}, {'C', 3},  {'D', 2}, {'E', 1}, {'F', 4}, {'G', 2},
                       {'H', 4}, {'I', 1}, {'J', 8},  {'K', 5}, {'L', 1}, {'M', 3}, {'N', 1},
                       {'O', 1}, {'P', 3}, {'Q', 10}, {'R', 1}, {'S', 1}, {'T', 1}, {'U', 1},
                       {'V', 4}, {'W', 4}, {'X', 8},  {'Y', 4}, {'Z', 10}};

int main(void)
{
    char word1[45];
    char word2[45];
    printf("Player 1: ");
    scanf("%s", word1);
    printf("Player 2: ");
    scanf("%s", word2);

    int score1 = get_score(word1);
    int score2 = get_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int get_score(char *word)
{
    int score = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        int word_letter = word[i];

        for (int j = 0; j < 26; j++)
        {
            int alphabet_letter = alphabet[j][0];

            if ((word_letter == alphabet_letter) || ((word_letter - 32) == alphabet_letter))
            {
                score += alphabet[j][1];
                break;
            }
        }
    }

    return score;
}

