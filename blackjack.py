import random

def make_deck():
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    deck = [[num + ' of ' + suit for suit in suits] for num in numbers]
    deck = [card for lst in deck for card in lst]
#     deck = random.shuffle(deck)
    deck_dict = {card: int(card[:2]) if card[:2].isdigit() else int(card[0]) if card[0].isdigit() else 'choose' if card[0] == 'a' else 10 for card in deck}
    random.shuffle(deck)
    return deck, deck_dict
         
def ace_assignment(lst):
#     print(lst)
    sets = []
    length = len(lst)
    current_set = [None for i in lst]
    def set_helper2(lst, set_length, current_set, i = 0):
        if i == length:
            sets.append(current_set)
        elif lst[i] == 'choose':
            current_set1, current_set2 = current_set[:i] + [1] + current_set[i + 1:], current_set[:i] + [11] + current_set[i + 1:]
            set_helper2(lst, length, current_set1, i + 1)
            set_helper2(lst, length, current_set2, i + 1)
        else:
            current_set1, current_set2 = current_set[:i] + [lst[i]] + current_set[i + 1:], current_set
            set_helper2(lst, length, current_set1, i + 1)
            set_helper2(lst, length, current_set2, i + 1)
    
    
    set_helper2(lst, length, current_set, 0)
#     print(sets)
    sets = [sum(s) for s in sets if None not in s and sum(s) <= 21]
    if len(sets) == 0:
        return 'bust'
    
    return max(sets)

def hand(deck, computer = False, cards = None):
    if not cards:
        if not computer:
            cards = [deck.pop(), deck.pop()]
            return cards
        cards = [deck.pop(), deck.pop()]
        return cards
    cards.append(deck.pop())
    return cards

def score(cards, deck_dict):
    for card in cards: 
        if deck_dict[card] == 'choose':
            total_score = ace_assignment([deck_dict[card] for card in cards])
            return total_score
    total_score = sum(deck_dict[card] for card in cards)
    if total_score > 21:
        return 'bust'
    return total_score

def turn(cards, deck, deck_dict, score ,computer = False, split = False):
    if computer:
#         print(score)
        if score < 17:
            cards = hand(deck, computer = True, cards = cards)
            return 'twist', cards
        return 'stick', cards
    inputs = ['s', 't', 'd', 'b']
    while True:
        print("""(s)tick, (t)wist, (d)ivide, (b)et""")
        player_decision = input('>').lower()
        if player_decision in inputs:
            if player_decision == 'b':
                if split or len(cards) != 2:
                    continue
                cards = hand(deck, computer = False, cards = cards)
                return 'bet', cards
            if player_decision == 't':
                cards = hand(deck, computer = False, cards = cards)
                return 'twist', cards
            elif player_decision == 'd':
                if cards[0][0] != cards[1][0] or split:
#                     print(cards[0][0], cards[1][0])
                    continue
                cards = [[card] for card in cards]
                return 'divide', cards
            return 'stick', cards

def decide_winner(player_score, dealer_score):
    if player_score == 'bust':
        if dealer_score == 'bust':
            return 'No winner. Both of you are bust', 'draw'
        return 'Dealer wins. You are bust', 'dealer'
    elif dealer_score == 'bust':
        return 'You are the winner. Dealer is bust', 'player'
    elif dealer_score == player_score:
        return 'No winner. You have the same score', 'draw'
    elif dealer_score < player_score:
        return 'You win', 'player'
    else:
        return 'You lose', 'dealer'

def print_cards(score, cards, player, dealer_start = False):
    suits_dict = {'hearts': chr(9829), 'diamonds': chr(9830), 'spades': chr(9824), 'clubs': chr(9827)}
    if dealer_start:
        print('DEALER: ?')
    else:
        print('{}: {}'.format(player, score))
    rows = ['', '', '', '', '']
    for card in cards:
        rank = card[0].upper() if card[0] != '1' else card[:2]
        suit = suits_dict[card[card.find('of') + 3:]]
        rank1 = rank + ' ' if len(rank) == 1 else rank
        rank2 = '_' + rank if len(rank) == 1 else rank
        rows[0] += ' ___  '
        if dealer_start:
            rows[1] += '|## | '
            rows[2] += '| # | '
            rows[3] += '|_##| '
            dealer_start = False
        else:
            rows[1] += '|{} | '.format(rank1)
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank2)
    for row in rows:
        print(row)

def play_blackjack():
    money = 1000
    while money:
        print('Money: {}'.format(money))
        while True:
            print('How much would you like to bet? Minimum of 100')
            bet = input('>')
            if bet.isdigit():
                bet = int(bet)
                if bet > money or bet < 100:
                    bet = 100
                money -= int(bet)
                break
        print('Bet: {}'.format(bet))
        deck, deck_dict = make_deck()
        cards, dealer = hand(deck), hand(deck, computer = True)
        print_cards(score(dealer, deck_dict), dealer, 'DEALER', dealer_start = True)
        while True:
    #         print(cards)
            player_score = score(cards, deck_dict)
            print_cards(player_score, cards, 'PLAYER')
            if player_score == 'bust':
                print('You are bust.')
                break
            player_decision, cards = turn(cards, deck, deck_dict, player_score)
            if player_decision == 'stick':
                print('Player sticks')
                break
            elif player_decision == 'bet':
                if money - bet >= 0:
                    money -= bet
                    bet += bet
                    print('bet incresead to: {}'.format(bet))
            elif player_decision == 'divide':
                new_hands = {}
                for single_hand in cards:
                    while True:
                        if money - bet >= 0:
                            money -= bet
                            bet += bet
                            print('New bet: {}'.format(bet))
#                         print(single_hand)
                        player_score = score(single_hand, deck_dict)
                        print_cards(player_score, single_hand, 'PLAYER')
                        if player_score == 'bust':
                            print('You are bust.')
    #                         new_hands[player_score] = single_hand
                            break
                        player_decision, cards = turn(single_hand, deck, deck_dict, player_score, split = True)
                        if player_decision == 'stick':
                            print('Player sticks')
                            new_hands[player_score] = single_hand
                            break
                key = sorted(new_hands.keys(), key=lambda x: (x == 'bust', x))[-1]
                player_score, cards = key, new_hands[key]          
                break
        while True:
            dealer_score = score(dealer, deck_dict)
            print_cards(dealer_score, dealer, 'DEALER')
            if dealer_score == 'bust':
                print('Dealer bust')
                break
            computer_decision, dealer = turn(dealer, deck, deck_dict, dealer_score, computer = True)
            if computer_decision == 'stick':
                print('Dealer sticks')
                break
        print(decide_winner(player_score, dealer_score)[0])
        if decide_winner(player_score, dealer_score)[1] == 'player':
            money += bet * 2
            print('You win {}'.format(bet))
        elif decide_winner(player_score, dealer_score)[1] == 'draw':
            money += bet
        if money == 0:
            print('You are out of money. GAME OVER')
            break
        elif money >= 3000:
            print('You have {} Money. YOU WIN'.format(money))
            break
        while True:
            print('Would you like to play again? y/n')
            keep_playing = input('>').lower()
            if keep_playing in ['y', 'n']:
                break
        if keep_playing == 'n':
            break
    return

play_blackjack()