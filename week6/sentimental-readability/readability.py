def main():
    text = input("Text: ")
    letters = 0
    words = 1
    sentences = 0

    for char in text:
        letters += 1 if is_alphabetical(char) else 0
        words += is_blank(char)
        sentences += is_punctuation(char)

    average_letters = (letters / words) * 100
    average_sentences = (sentences / words) * 100
    index = int(0.0588 * average_letters - 0.296 *
                average_sentences - 15.8 + 0.5)

    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def is_alphabetical(letter):
    return 1 if ('a' <= letter <= 'z' or 'A' <= letter <= 'Z') else 0


def is_blank(letter):
    return 1 if letter == ' ' else 0


def is_punctuation(letter):
    return 1 if letter in '.?!' else 0


main()

