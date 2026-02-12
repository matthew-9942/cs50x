#include <stdio.h>

int is_lowercase(char letter);
int is_uppercase(char letter);
int get_length(char *string);
int is_key_valid(char *key);
int get_position(char letter, int min_range);

int main(int argc, char *argv[])
{
    char *key = argv[1];
    if (argc != 2)
    {
        printf("Usage: ./substitution key");
        return 1;
    }
    if (get_length(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.");
        return 1;
    }

    int valid = is_key_valid(key);

    if (!valid)
    {
        printf("Key must be unique.");
        return 1;
    }

    char plaintext[1024];
    printf("plaintext:  ");
    fgets(plaintext, 1024, stdin);
    int plaintext_length = get_length(plaintext);
    char ciphertext[plaintext_length + 1];
    ciphertext[plaintext_length] = '\0';

    for (int i = 0; plaintext[i] != '\0'; i++)
    {
        char letter = plaintext[i];

        if (is_uppercase(letter))
        {
            int position = get_position(letter, 65);
            char key_char = key[position];

            if (is_lowercase(key_char))
            {
                key_char -= 32;
            }

            ciphertext[i] = key_char;
            continue;
        }
        else if (is_lowercase(letter))
        {
            int position = get_position(letter, 97);
            char key_char = key[position];

            if (is_uppercase(key_char))
            {
                key_char += 32;
            }

            ciphertext[i] = key_char;
            continue;
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    printf("ciphertext: %s", ciphertext);
    return 0;
}

int is_lowercase(char letter)
{
    return (letter >= 'a' && letter <= 'z') ? 1 : 0;
}

int is_uppercase(char letter)
{
    return (letter >= 'A' && letter <= 'Z') ? 1 : 0;
}

int get_length(char *string)
{
    int length = 0;
    for (int i = 0; string[i] != '\0'; i++)
    {
        length++;
    }

    return length;
}

int is_key_valid(char *key)
{
    int is_valid = 0;
    int uniqueness[26][2] = {{'A', 0}, {'B', 0}, {'C', 0}, {'D', 0}, {'E', 0}, {'F', 0}, {'G', 0},
                             {'H', 0}, {'I', 0}, {'J', 0}, {'K', 0}, {'L', 0}, {'M', 0}, {'N', 0},
                             {'O', 0}, {'P', 0}, {'Q', 0}, {'R', 0}, {'S', 0}, {'T', 0}, {'U', 0},
                             {'V', 0}, {'W', 0}, {'X', 0}, {'Y', 0}, {'Z', 0}};

    for (int i = 0; key[i] != '\0'; i++)
    {
        char letter = key[i];

        for (int j = 0; j < 26; j++)
        {
            if (is_uppercase(letter) && letter == uniqueness[j][0])
            {
                uniqueness[j][1]++;
                break;
            }
            else if (is_lowercase(letter) && (letter - 32) == uniqueness[j][0])
            {
                uniqueness[j][1]++;
                break;
            }
            else
            {
                continue;
            }
        }
    }

    for (int i = 0; i < 26; i++)
    {
        if (uniqueness[i][1] != 1)
        {
            is_valid = 0;
            break;
        }
        is_valid = 1;
    }

    return is_valid;
}

int get_position(char letter, int min_range)
{
    return letter - min_range;
}

