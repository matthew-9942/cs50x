#include <cs50.h>
#include <stdio.h>

int get_change_oved(void);

int main(void)
{
    int coin_count = 0;
    int change_oved = get_change_oved();
    int coins_length = 4;
    int coins[] = {25, 10, 5, 1}; // can be customized

    while (change_oved > 0)
    {
        for (int i = 0; i < coins_length; i++)
        {
            while (change_oved >= coins[i])
            {
                change_oved -= coins[i];
                coin_count++;
            }
        }
    }

    printf("%i\n", coin_count);
}

int get_change_oved(void)
{
    int change_oved;
    do
    {
        change_oved = get_int("Change oved: ");
    }
    while (change_oved < 0);

    return change_oved;
}

