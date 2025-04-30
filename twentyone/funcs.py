import random as rnd

class TwentyOneGame():
    def __init__(self):
        self.balance = 0
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []
        self.deck = self.kruchu_verchu()

    def set_balance(self):
        while True:
            try:
                self.balance = int(input("Введите размер депозита: "))
                if self.balance <= 0:
                    print("Самый умный?")
                else:
                    print(f"Ваш баланс: {self.balance} монет.")
                    break
            except ValueError:
                print("Смешно, еб*ть, давай-давай нападай.")

    def place_bet(self):
        while True:
            try:
                self.bet = int(input("Введите размер ставки: "))
                if self.bet <= 0:
                    print("Самый умный?")
                elif self.bet > self.balance:
                    print("Ты слишком нищий для такой ставки. Давай додеп.")
                else:
                    self.balance -= self.bet
                    if self.bet == self.balance + self.bet:
                        print("Вы поставили всё! Хорошая уверенность...")
                    else:
                        print(f"Ставка {self.bet} принята. Остаток: {self.balance}")
                    break
            except ValueError:
                print("Вводи число, а не буквы!")

    def kruchu_verchu(self):
        mast = ['♥', '♦', '♣', '♠']
        znach = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [(m, z) for m in mast for z in znach]
        rnd.shuffle(deck)
        return deck

    def calculate_hand(self, hand):
        znach = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
                 '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}
        total = sum(znach[card[1]] for card in hand)
        aces = sum(1 for card in hand if card[1] == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def deal_initial_cards(self):
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def show_hands(self, reveal_dealer=False):
        if reveal_dealer:
            print("\nКарты дилера:")
        else:
            print("\nКарты дилера (одна скрыта):")
        if reveal_dealer:
            for card in self.dealer_hand:
                print(f"{card[1]}{card[0]}  ", end="")
        else:
            print(f"{self.dealer_hand[0][1]}{self.dealer_hand[0][0]}  [скрыта]")
        print("\nВаши карты:")
        for card in self.player_hand:
            print(f"{card[1]}{card[0]}  ", end="")
        print()
    
    def player_turn(self):
        while True:
            action = input("\nВаш ход:\n(1) Взять карту  \n(2) Остановиться: ")
            if action == '1':
                self.player_hand.append(self.deck.pop())
                self.show_hands()
                if self.calculate_hand(self.player_hand) > 21:
                    print("\nПеребор! Вы проиграли.")
                    return False
            elif action == '2':
                return True
            else:
                print("Некорректный ввод. Выберите 1 или 2.")

    def dealer_turn(self):
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
            print(f"\nДилер берет карту: {self.dealer_hand[-1][1]}{self.dealer_hand[-1][0]}")
        self.show_hands(reveal_dealer=True)
        return self.calculate_hand(self.dealer_hand) <= 21

    def who_is_winner(self):
        player_score = self.calculate_hand(self.player_hand)
        dealer_score = self.calculate_hand(self.dealer_hand)
        print("\n=== Результат ===")
        print(f"Ваши очки: {player_score}  |  Очки дилера: {dealer_score}")
        if player_score > 21:
            print("Вы перебрали. Дилер побеждает. Анлак + Невезуха")
            return -1
        elif dealer_score > 21:
            print("Дилер перебрал. Вы побеждаете! Сюдааа")
            return 1
        elif player_score > dealer_score:
            print("Вы побеждаете!")
            return 1
        elif player_score < dealer_score:
            print("Дилер побеждает.")
            return -1
        else:
            print("Ничья!")
            return 0

    def play_round(self):
        print("====================")
        if len(self.deck) < 6:
            self.deck = self.create_deck()
            print("Карт было слишком мало. Колода обновлена.")
        self.place_bet()
        self.deal_initial_cards()
        self.show_hands()
        if self.player_turn():
            dealer_ok = self.dealer_turn()
            result = self.who_is_winner()
            if result == 1:
                self.balance += 2 * self.bet
                print(f"Вы выиграли {2 * self.bet}!")
            elif result == 0:
                self.balance += self.bet
                print("Возврат ставки.")

        print(f"\nТекущий баланс: {self.balance}")
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []

    def start_game(self):
            print("\n♠♥♦♣ Добро пожаловать в 21! ♠♥♦♣")
            self.set_balance()
            while self.balance > 0:
                self.play_round()
                if input("\nСыграем еще? (y/n): ").lower() not in  ['y', 'н', 1, 'yes', 'да', '']:
                    break
            print(f"\nИгра окончена. Ваш баланс: {self.balance}")













