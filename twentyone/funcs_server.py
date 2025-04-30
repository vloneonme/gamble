import random as rnd


class TwentyOneGame():
    def __init__(self):
        self.balance = 0
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []
        self.deck = self.kruchu_verchu()
        self.is_player_turn = True
        self.is_dealer_turn = True

    def set_balance(self, choice):
        if choice is None:
            return self.set_balance, "Введите размер депозита: ", True
        try:
            self.balance = int(choice)
            if self.balance <= 0:
                return self.set_balance, "Самый умный?", True
            else:
                return self.play_round, f"Ваш баланс: {self.balance} монет.", False
        except ValueError:
            return self.set_balance, "Смешно, еб*ть, давай-давай нападай.", True

    def place_bet(self, choice):
        if choice is None:
            return self.place_bet, "Введите размер ставки: ", True
        try:
            self.bet = int(choice)
            if self.bet <= 0:
               return self.place_bet, "Самый умный?", True
            elif self.bet > self.balance:
                return self.place_bet, "Ты слишком нищий для такой ставки. Давай додеп.", True
            else:
                self.balance -= self.bet
                if self.bet == self.balance + self.bet:
                    return self.play_round, "Вы поставили всё! Хорошая уверенность...", False
                else:
                    return self.play_round, f"Ставка {self.bet} принята. Остаток: {self.balance}", False
        except ValueError:
            return self.place_bet, "Вводи число, а не буквы!", True

    def kruchu_verchu(self):
        mast = ['♥', '♦', '♣', '♠']
        znach = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [(m, z) for m in mast for z in znach]
        rnd.shuffle(deck)
        return deck

    def calculate_hand(self, hand):
        znach = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                 '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
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
        s = ""
        if reveal_dealer:
            s = "\nКарты дилера:\n"
        else:
            s = "\nКарты дилера (одна скрыта):\n"
        if reveal_dealer:
            for card in self.dealer_hand:
                s = s + f"{card[1]}{card[0]}  "
            s = s[:-1]
        else:
            s = s + f"{self.dealer_hand[0][1]}{self.dealer_hand[0][0]}  [скрыта]"
        s = s + "\nВаши карты:"
        for card in self.player_hand:
            s = s + f"{card[1]}{card[0]}  "
            s = s[:-1]
        return s

    def player_turn(self, choice):
        if choice is None:
            return self.player_turn, "\nВаш ход:\n(1) Взять карту  \n(2) Остановиться: ", True
        if choice == '1':
            self.player_hand.append(self.deck.pop())
            s = self.show_hands()
            if self.calculate_hand(self.player_hand) > 21:
                self.is_player_turn = False
                self.is_dealer_turn = False
                return self.play_round, s + "\nПеребор! Вы проиграли.", False
            else:
                return self.player_turn, s, False

        elif choice == '2':
            self.is_player_turn = False
            return self.play_round, "", False
        else:
            return self.player_turn,  "Некорректный ввод. Выберите 1 или 2.", True

    def dealer_turn(self):
        s = ""
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
            s = s + f"\nДилер берет карту: {self.dealer_hand[-1][1]}{self.dealer_hand[-1][0]}"
        s = s + self.show_hands(reveal_dealer=True)
        self.is_dealer_turn = False
        return s

    def who_is_winner(self):
        player_score = self.calculate_hand(self.player_hand)
        dealer_score = self.calculate_hand(self.dealer_hand)
        s = "\n=== Результат ===\n"
        s = s + f"Ваши очки: {player_score}  |  Очки дилера: {dealer_score}\n"
        if player_score > 21:
            return -1, s + "Вы перебрали. Дилер побеждает. Анлак + Невезуха\n"
        elif dealer_score > 21:
            return 1, s +"Дилер перебрал. Вы побеждаете! Сюдааа\n"
        elif player_score > dealer_score:
            return 1, s + "Вы побеждаете!\n"
        elif player_score < dealer_score:
            return -1, s + "Дилер побеждает.\n"
        else:
            return 0, s + "Ничья!\n"

    def play_round(self, choice):
        if self.balance <= 0:
            return -1, f"\nИгра окончена. Ваш баланс: {self.balance}", True
        if self.bet == 0:
            return self.place_bet, "====================", False
        if len(self.deck) < 6:
            self.deck = self.create_deck()
            return self.play_round, "Карт было слишком мало. Колода обновлена.", False

        if self.is_player_turn:
            self.deal_initial_cards()
            return self.player_turn, self.show_hands(), False

        s = ""
        if self.is_dealer_turn:
            return self.play_round, self.dealer_turn(), False
        result, message = self.who_is_winner()
        print(result, message)
        if result == 1:
            self.balance += 2 * self.bet
            s =  message + f"Вы выиграли {2 * self.bet}!\n"
        elif result == 0:
            self.balance += self.bet
            s =  message + "Возврат ставки.\n"

        s = s + f"\nТекущий баланс: {self.balance}\n"
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []
        return self.next_game, s, False

    def start_game(self, choice):
        return self.set_balance, "\n♠♥♦♣ Добро пожаловать в 21! ♠♥♦♣", False

    def next_game(self, choice):
        if choice is None:
            return self.next_game, "\nСыграем еще? (y/n): ", True
        else:
            if choice.lower() not in ['y', 'н', 1, 'yes', 'да', '']:
                return -1, f"\nИгра окончена. Ваш баланс: {self.balance}", False
            return self.play_round













