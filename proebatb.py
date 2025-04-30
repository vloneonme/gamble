from Danya_game.twentyone import funcs_server
from Danya_game.twentyone import funcs

def main():
    print("Игры: \n (1) - Двадцать одно \n (0) - Выход")
    while True:
        n = input("Ввод: ")
        try:
            n = int(n)
        except ValueError:
            print("Число нужно ввести, умник, блять")
            continue
        if n == 0:
            print("\nНаигрался, значит. \nКонец работы программы")
            break
        elif n == 1:
            print("Вы выбрали сыграть в Двадцать Одно")
            funcs.TwentyOneGame().start_game()
        else:
            print("Неизвестный вариант. Выберите 0 или 1")

def choosingGame(choice):
    if not choice:
        return choosingGame, "Игры: \n (1) - Двадцать одно \n (0) - Выход", True
    n = 0
    try:
        n = int(choice)
    except ValueError:
        return choosingGame, "Число нужно ввести, умник, блять", True
    if n == 1:
        return funcs_server.TwentyOneGame().start_game, "Вы выбрали сыграть в Двадцать Одно", False
    elif n == 0:
        return -1, "\nНаигрался, значит. \nКонец работы программы", False
    else:
        return choosingGame, "Неизвестный вариант. Выберите 0 или 1", True

if __name__ == "__main__":
    main()



