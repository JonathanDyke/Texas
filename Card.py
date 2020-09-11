import Deck

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{Deck.Deck().ranks[self.rank]} of {Deck.Deck().suits[self.suit]}'

    def __repr__(self):
        return f'{self.rank}, {self.suit}'
