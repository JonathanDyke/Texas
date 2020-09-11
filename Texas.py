import itertools
from Deck import Deck
from Card import Card
from Player import Player

def new_game(number):
    print('New Game\n')
    game_deck = Deck()
    game_deck.shuffle()
    active_players = []
    for i in range(number):
        player = Player(input('Player name: '))
        active_players.append(player)
    return game_deck, active_players

def new_round(game_deck, active_players):
    print('\nNew Round\n')
    chips_pot = 0
    current_round_players = []
    for player in list(active_players):
        if player.chips == 0:
            active_players.remove(player)
        player.hand = []
    for player in active_players:
        current_round_players.append(player)
        for i in range(2):
            card = game_deck.draw_card()
            player.hand.append(card)
    bet = 5
    prev_move = None
    betting_finished = False
    while not betting_finished:
        if len(current_round_players) == 0:
            betting_finished = True
            break
        else:
            for player in list(current_round_players):
                player_hand_str = ', '.join([str(i) for i in player.hand])
                print(f'Player: {player}', f'\nHand: {player_hand_str}', f'\nCurrent bet: {bet}')
                if bet == player.previous_bet:
                    betting_finished = True
                    break
                elif bet == 5:
                    completed = False
                    while completed == False:
                        move = input('Fold, call (5 chips), or raise: ')
                        if move in ('Fold', 'fold'):
                            current_round_players.remove(player)
                            completed = True
                        elif move in ('Call', 'call'):
                            player.call(5)
                            chips_pot += 5
                            completed = True
                        elif move in ('Raise', 'raise'):
                            raise_amount = 0
                            while not raise_amount:
                                try:
                                    raise_amount = int(input('Raise to what amount? '))
                                    if raise_amount <= bet:
                                        print(f'Current bet is {bet}, raise must be higher')
                                        raise_amount = 0
                                except ValueError:
                                    print('Raise amount must be an integer')
                            if raise_amount >= player.chips:
                                raise_amount = player.chips
                                print(f'{str(player)} all in with {raise_amount} chips')
                            player.raise_bet(raise_amount)
                            bet = raise_amount
                            chips_pot += raise_amount
                            completed = True
                        else:
                            print('Please enter fold, call or raise ')
                else:
                    completed = False
                    while completed == False:
                        move = input('Call or raise? ')
                        if move in ('Call', 'call'):
                            chips_pot += bet - player.previous_bet
                            player.call(bet - player.previous_bet)
                            completed = True
                        elif move in ('Raise', 'raise'):
                            while True:
                                try:
                                    raise_amount = int(input('Raise to what amount? '))
                                    if raise_amount <= bet:
                                        print(f'Current bet is {bet}, raise must be higher')
                                    else:
                                        break
                                except ValueError:
                                    print('Raise amount must be an integer')
                            if raise_amount >= player.chips:
                                raise_amount = player.chips
                                print(f'{str(player)} all in with {raise_amount} chips')
                            player.raise_bet(raise_amount)
                            bet = raise_amount
                            chips_pot += raise_amount - player.previous_bet
                            completed = True
    for player in current_round_players:
        player.previous_bet = 0
    return current_round_players, chips_pot

def one_player_left(player, chips_pot, active_players):
    print(f'\nWinning player: {player}, winning {chips_pot} chips')
    player.chips += chips_pot
    for player in list(active_players):
        if player.chips == 0:
            active_players.remove(player)
        player.hand = []
    return active_players

def flop(game_deck):
    game_deck.five = []
    for i in range(3):
        flop_card = game_deck.draw_card()
        game_deck.five.append(flop_card)
        table_cards_str = ', '.join([str(i) for i in game_deck.five])
    print(f'\nFlop cards: {table_cards_str}')
    return game_deck.five

def river(game_deck):
    river_card = game_deck.draw_card()
    game_deck.five.append(river_card)
    table_cards_str = ', '.join([str(i) for i in game_deck.five])
    print(f'\nRiver cards: {table_cards_str}')
    return game_deck.five

def turn(game_deck):
    turn_card = game_deck.draw_card()
    game_deck.five.append(turn_card)
    table_cards_str = ', '.join([str(i) for i in game_deck.five])
    print(f'\nTurn cards: {table_cards_str}')
    return game_deck.five

def betting(current_round_players, chips_pot, cards):
    bet = 0
    prev_move = None
    betting_finished = False
    while not betting_finished:
        for player in list(current_round_players):
            if bet == player.previous_bet and bet != 0:
                betting_finished = True
                final_player = player
            elif prev_move == 'check' or prev_move == None:
                if player.checked == True:
                    for player in current_round_players:
                        player.checked = False
                        final_player = player
                    for i in range(current_round_players.index(final_player) + 1):
                        current_round_players.append(current_round_players.pop(0))
                    return current_round_players, chips_pot
                table_cards_str = ', '.join([str(i) for i in cards])
                player_hand_str = ', '.join([str(i) for i in player.hand])
                print(f'\nPlayer: {player}\nTable cards: {table_cards_str}\nYour hand: '
                f'{player_hand_str}, \nYour chips: {player.chips}')
                completed = False
                while completed == False:
                    move = input('Check or Bet: ')
                    if move in ('Check', 'check'):
                        player.check()
                        completed = True
                        prev_move = 'check'
                    elif move in ('Bet', 'bet'):
                        bet_amount = 0
                        while not bet_amount:
                            try:
                                bet_amount = int(input('Bet how much? '))
                            except ValueError:
                                print('Bet must be a number')
                        if bet_amount >= player.chips:
                            bet_amount = player.chips
                            print(f'{str(player)} all in with {bet_amount} chips')
                        player.bet(bet_amount)
                        chips_pot += bet_amount
                        bet = bet_amount
                        completed = True
                        prev_move = 'bet'
                    else:
                        print('Please enter either check or bet')
            elif prev_move in ['bet', 'raise', 'call']:
                table_cards = ', '.join([str(i) for i in cards])
                print(f'\nPlayer: {player}\nTable cards: {table_cards}\nYour hand:'
                f'{[str(i) for i in player.hand]}, \nYour chips: {player.chips}')
                completed = False
                while completed == False:
                    print(f'Current bet is {bet} chips')
                    move = input('Raise, call or fold: ')
                    if move in ('Call', 'call'):
                        if bet - player.previous_bet >= player.chips:
                            call_amount = player.chips
                            print(f'{str(player)} all in with {call_amount} chips')
                        else:
                            call_amount = bet - player.previous_bet
                        chips_pot += call_amount
                        player.call(call_amount)
                        completed = True
                        prev_move == 'call'
                    elif move in ('Raise', 'raise'):
                        raise_amount = 0
                        while not raise_amount:
                            try:
                                raise_amount = int(input('Raise to what amount? '))
                                if raise_amount <= bet:
                                    print(f'Current bet is {bet}, raise must be higher')
                                    raise_amount = 0
                            except ValueError:
                                print('Raise amount must be an integer')
                        if raise_amount >= player.chips:
                            raise_amount = player.chips
                            print(f'{str(player)} all in with {raise_amount} chips')
                        player.raise_bet(raise_amount)
                        chips_pot += raise_amount
                        bet = raise_amount
                        completed = True
                        prev_move = 'raise'
                    elif move in ('Fold', 'fold'):
                        current_round_players.remove(player)
                        completed = True
                    else:
                        print('Please enter raise, call or fold')
                pass
    for player in current_round_players:
        player.checked = False
        player.previous_bet = 0
    for i in range(current_round_players.index(final_player) + 1):
        current_round_players.append(current_round_players.pop(0))
    return current_round_players, chips_pot

def get_winner(current_round_players, cards, chips_pot, active_players):
    player_scores = {}
    for player in current_round_players:
        max_score = 0
        hand = player.hand + cards
        seen_numbers = {}
        seen_suits = {}

        for i in hand:
            if i.rank in seen_numbers:
                seen_numbers[i.rank] += 1
            else:
                seen_numbers[i.rank] = 1
            if i.suit in seen_suits:
                seen_suits[i.suit] += 1
            else:
                seen_suits[i.suit] = 1

        for i, j in zip(seen_suits.keys(), seen_suits.values()):
            if j >= 5:
                flush_list = sorted([k.rank for k in hand if k.suit == i]) # ranks
                c = itertools.count()
                val = max((list(g) for _, g in itertools.groupby(flush_list, lambda x: x-next(c))), \
                key=len)
                if len(val) >= 5:
                    if 14 in val:
                        max_score = 9 # Royal Flush score
                    else:
                        max_score = 8.5 # Straight Flush score
                else:
                    score = 5.5 # Flush
                    if score >= max_score:
                        max_score = score
        for i, j in zip(seen_numbers.keys(), seen_numbers.values()):
            if j == 4:
                score = 7 + (i * (1/14)) # 4 of a Kind
                if score > max_score:
                    max_score = score
            elif j == 3:
                first_three = i
                for second_three, t in zip(seen_numbers.keys(), seen_numbers.values()):
                    if t == 2:
                        score = 6 + (i * (1/14)) # Full House
                        if score > max_score:
                            max_score = score
                    elif t == 3:
                        if second_three != first_three:
                            if second_three >= first_three:
                                score = 6 + (second_three * (1/14)) # Full House
                                if score > max_score:
                                    max_score = score
                            else:
                                score = 6 + (first_three * (1/14)) # Full House
                                if score > max_score:
                                    max_score = score
                score = 3 + (i * (1/14)) # 3 of a Kind
                if score > max_score:
                    max_score = score
            elif j == 2:
                first_pair = i
                for second_pair, t in zip(seen_numbers.keys(), seen_numbers.values()):
                    if t == 2:
                        if second_pair != first_pair:
                            if second_pair >= first_pair:
                                score = 2 + (second_pair * (1/14)) # 2 pair
                                if score > max_score:
                                    max_score = score
                            else:
                                score = 2 + (first_pair * (1/14)) # 2 pair
                                if score > max_score:
                                    max_score = score
                score = 1 + (i * (1/14)) # 1 pair
                if score > max_score:
                    max_score = score
            else:
                # Check for straight
                straight_list = sorted([k.rank for k in hand])
                c = itertools.count()
                val = max((list(g) for _, g in itertools.groupby(straight_list, lambda x: x-next(c))), \
                key=len)
                if len(val) >= 5:
                    score = 4 + (i * (1/14)) # Straight
                    if score > max_score:
                        max_score = score
                # Finally check max card
                max_card = max(seen_numbers) # High card
                score = max_card * (1/14)
                if score > max_score:
                    max_score = score
        player_scores[player] = max_score

    winning_score = max(player_scores.values())
    winning_players = [k for k,v in player_scores.items() if v == winning_score]
    winning_players_str = (', '.join([str(i) for i in winning_players]))
    if len(winning_players) > 1:
        print(f'\nWinning players: {winning_players_str}, winning {chips_pot / len(winning_players)} chips')
    else:
        print(f'\nWinning player: {winning_players_str}, winning {chips_pot} chips')
    for player in winning_players:
        player.chips += chips_pot / len(winning_players)
    return active_players

def all_in(current_round_players, chips_pot, game_deck, active_players, cards=None):
    if not cards:
        flop_cards = flop(game_deck)
        river_cards = river(game_deck)
        turn_cards = turn(game_deck)
        active_players = get_winner(current_round_players, turn_cards, chips_pot, active_players)
        for player in list(active_players):
            if player.chips == 0:
                active_players.remove(player)
            player.hand = []
        return active_players
    elif len(cards) == 3:
        river_cards = river(game_deck)
        turn_cards = turn(game_deck)
        active_players = get_winner(current_round_players, turn_cards, chips_pot, active_players)
        for player in list(active_players):
            if player.chips == 0:
                active_players.remove(player)
            player.hand = []
        return active_players
    elif len(cards) == 4:
        turn_cards = turn(game_deck)
        active_players = get_winner(current_round_players, turn_cards, chips_pot, active_players)
        for player in list(active_players):
            if player.chips == 0:
                active_players.remove(player)
            player.hand = []
        return active_players

def full_round(game_deck, active_players):
    new_game_players, chips_pot = new_round(game_deck, active_players)
    if len(new_game_players) > 1:
        pass
    elif len(new_game_players) == 1:
        active_players = one_player_left(new_game_players[0], chips_pot, active_players)
        return active_players
    else:
        return active_players
    if len([player for player in new_game_players if player.chips == 0]) == len(new_game_players) or \
    len([player for player in new_game_players if player.chips == 0]) == len(new_game_players) - 1:
        active_players = all_in(new_game_players, chips_pot, game_deck, active_players)
        return active_players
    flop_cards = flop(game_deck)
    flop_players, chips_pot = betting(new_game_players, chips_pot, flop_cards)
    if len(flop_players) > 1:
        pass
    elif len(flop_players) == 1:
        active_players = one_player_left(flop_players[0], chips_pot, active_players)
        return active_players
    if len([player for player in flop_players if player.chips == 0]) == len(flop_players) or \
    len([player for player in flop_players if player.chips == 0]) == len(flop_players) - 1:
        active_players = all_in(flop_players, chips_pot, game_deck, active_players, flop_cards)
        return active_players
    river_cards = river(game_deck)
    river_players, chips_pot = betting(flop_players, chips_pot, river_cards)
    if len(river_players) > 1:
        pass
    elif len(river_players) == 1:
        active_players = one_player_left(river_players[0], chips_pot, active_players)
        return active_players
    if len([player for player in river_players if player.chips == 0]) == len(river_players) or \
    len([player for player in river_players if player.chips == 0]) == len(river_players) - 1:
        active_players = all_in(river_players, chips_pot, active_players, river_cards)
        return active_players
    turn_cards = turn(game_deck)
    turn_players, chips_pot = betting(river_players, chips_pot, turn_cards)
    if len(turn_players) > 1:
        pass
    elif len(turn_players) == 1:
        active_players = one_player_left(turn_players[0], chips_pot, active_players)
        return active_players
    if len([player for player in turn_players if player.chips == 0]) == len(turn_players) or \
    len([player for player in turn_players if player.chips == 0]) == len(turn_players) - 1:
        active_players = all_in(turn_players, chips_pot, game_deck, active_players, turn_cards)
        return active_players
    active_players = get_winner(turn_players, turn_cards, chips_pot, active_players)
    return active_players

def play():
    while True:
        try:
            number_of_players = int(input('How many people are playing? '))
            if number_of_players <= 8 and number_of_players >= 2:
                break
            else:
                print('Number of players must be between 2 and 8')
        except ValueError:
            print('Number of players must be an integer')
    game_deck, active_players = new_game(number_of_players)
    while len(active_players) >= 2:
        active_players = full_round(game_deck, active_players)
    print(f'Game Winner: {active_players[0]}')

if __name__ == '__main__':
    play()
