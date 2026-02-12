#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

int is_lowercase(char letter);
int is_uppercase(char letter);
char get_cipherletter(char letter, int min_range, int max_range, int key);
int get_length(char *string);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; argv[1][i] != '\0'; i++) {
        if (!isdigit(argv[1][i])) {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);
    char plaintext[1024];
    printf("plaintext:  ");
    fgets(plaintext, 1024, stdin);
    int plaintext_length = get_length(plaintext);
    char ciphertext[plaintext_length + 1];

    for (int i = 0; plaintext[i] != '\0'; i++) {
        char letter = plaintext[i];

        if (is_uppercase(letter)) {
            ciphertext[i] = get_cipherletter(letter, 65, 90, key);
        } else if (is_lowercase(letter)) {
            ciphertext[i] = get_cipherletter(letter, 97, 122, key);
        } else {
            ciphertext[i] = letter;
        }
    }

    ciphertext[plaintext_length] = '\0';
    printf("ciphertext: %s", ciphertext);
    return 0;
}

int is_lowercase(char letter) {
    return (letter >= 'a' && letter <= 'z') ? 1 : 0;
}

int is_uppercase(char letter) {
    return (letter >= 'A' && letter <= 'Z') ? 1 : 0;
}

char get_cipherletter(char letter, int min_range, int max_range, int key) {
    int alphabet_size = 26;
    int position = letter - min_range;
    int new_position = (position + key) % alphabet_size;
    return min_range + new_position;
}

int get_length(char *string) {
    int length = 0;
    for (int i = 0; string[i] != '\0'; i++) {
        length++;
    }

    return length;
}
