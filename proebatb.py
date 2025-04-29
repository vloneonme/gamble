from twentyone import funcs

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

if __name__ == "__main__":
    main()



