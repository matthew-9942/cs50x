#include <cs50.h>
#include <math.h>
#include <stdio.h>

long get_creditcard_number();
int is_valid(long creditcard_number);
int get_length(long creditcard_number);

int main(void)
{
    long creditcard_number = get_creditcard_number();
    int valid = is_valid(creditcard_number);
    int length = get_length(creditcard_number);
    int first_digits = creditcard_number / pow(10, (length - 2));
    int first_digit = first_digits / 10;

    if (!valid || (length != 13 && length != 15 && length != 16))
    {
        printf("INVALID\n");
    }
    else
    {
        if (length == 15 && (first_digits == 34 || first_digits == 37))
        {
            printf("AMEX\n");
        }
        else if (length == 16 && (first_digits == 51 || first_digits == 52 || first_digits == 53 ||
                                  first_digits == 54 || first_digits == 55))
        {
            printf("MASTERCARD\n");
        }
        else if ((length == 13 || length == 16) && first_digit == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

    return 0;
}

long get_creditcard_number()
{
    long creditcard_number;
    do
    {
        creditcard_number = get_long("Number: ");
    }
    while (creditcard_number < 400000000);

    return creditcard_number;
}

int is_valid(long creditcard_number)
{
    int position = 1;
    int sum = 0;

    while (creditcard_number > 0)
    {
        int last_digit = creditcard_number % 10;
        creditcard_number /= 10;

        if (position % 2 == 0)
        {
            int digit = last_digit * 2;

            if (digit >= 10)
            {
                sum += (digit / 10) + (digit % 10);
            }
            else
            {
                sum += digit;
            }
        }
        else
        {
            sum += last_digit;
        }

        position++;
    }

    return (sum % 10 == 0);
}

int get_length(long creditcard_number)
{
    int length = 0;
    while (creditcard_number > 0)
    {
        length += 1;
        creditcard_number /= 10;
    }

    return length;
}

