import random
import Card

class Deck:
    def __init__(self):
        self.deck = []
        self.suits = {'S': 'Spades', 'C': 'Clubs', 'H': 'Hearts', 'D': 'Diamonds'}
        self.ranks = {2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', \
        8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
        self.five = []

        for i in self.ranks:
            for j in self.suits:
                self.deck.append(Card.Card(i, j))

    def __repr__(self):
        return ', '.join([str(i) for i in self.deck])

    def shuffle(self):
        return random.shuffle(self.deck)

    def draw_card(self):
        top_card = self.deck[0]
        self.deck.remove(top_card)
        return top_card
