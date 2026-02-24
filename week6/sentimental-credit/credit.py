def main():
    creditcard_number = get_creditcard_number()
    valid = is_valid(creditcard_number)
    length = get_length(creditcard_number)
    first_digits = creditcard_number // (10 ** (length - 2))
    first_digit = first_digits // 10

    if not valid or (length != 13 and length != 15 and length != 16):
        print("INVALID")
    else:
        if length == 15 and (first_digits == 34 or first_digits == 37):
            print("AMEX")
        elif length == 16 and (first_digits == 51 or first_digits == 52 or first_digits == 53 or
                               first_digits == 54 or first_digits == 55):
            print("MASTERCARD")
        elif (length == 13 or length == 16) and first_digit == 4:
            print("VISA")
        else:
            print("INVALID")


def get_creditcard_number():
    while True:
        try:
            creditcard_number = int(input("Number: "))
            if creditcard_number >= 400000000:
                return creditcard_number
        except ValueError:
            pass


def is_valid(creditcard_number):
    position = 1
    total = 0

    while creditcard_number > 0:
        last_digit = creditcard_number % 10
        creditcard_number //= 10

        if position % 2 == 0:
            digit = last_digit * 2
            if digit >= 10:
                total += (digit // 10) + (digit % 10)
            else:
                total += digit
        else:
            total += last_digit

        position += 1

    return total % 10 == 0


def get_length(creditcard_number):
    length = 0
    while creditcard_number > 0:
        length += 1
        creditcard_number //= 10
    return length


main()

