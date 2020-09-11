class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 1000
        self.hand = []
        self.hand_score = 0
        self.previous_bet = 0
        self.checked = False

    def __repr__(self):
        return self.name

    def check(self):
        self.checked = True

    def call(self, amount):
        self.chips -= amount
        self.previous_bet = amount

    def bet(self, amount):
        self.chips -= amount
        self.previous_bet = amount

    def raise_bet(self, amount):
        self.chips -= amount - self.previous_bet
        self.previous_bet = amount
