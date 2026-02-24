import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        return

    # Read database file into a variable
    database = []
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        strs = reader.fieldnames[1:]  # Skip "name" column
        for row in reader:
            database.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as f:
        sequence = f.read().strip()

    # Find longest match of each STR in DNA sequence
    counts = {str_: longest_match(sequence, str_) for str_ in strs}

    # Check database for matching profiles
    for person in database:
        if all(int(person[str_]) == counts[str_] for str_ in strs):
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run


main()

