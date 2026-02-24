def main():
    coins = [25, 10, 5, 1]  # can be customized
    coin_count = 0
    change_owed = get_change_owed()

    while change_owed > 0:
        for coin in coins:
            while change_owed >= coin:
                change_owed -= coin
                coin_count += 1

    print(coin_count)


def get_change_owed():
    while True:
        try:
            change_owed = round(float(input("Change owed: ")) * 100)
            if change_owed >= 0:
                return change_owed
        except ValueError:
            pass


main()

