import random

hearts, diamonds, spades, clubs = chr(9829), chr(9830), chr(9824), chr(9827)

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

def turn(cards, deck, deck_dict, score ,computer = False):
    if computer:
#         print(score)
        if score < 17:
            cards = hand(deck, computer = True, cards = cards)
            return 'twist', cards
        return 'stick', cards
    inputs = ['s', 't', 'd']
    while True:
        print("""(s)tick, (t)wist, (d)ivide """)
        player_decision = input('>').lower()
        if player_decision in inputs:
            if player_decision == 't':
                cards = hand(deck, computer = False, cards = cards)
                return 'twist', cards
            elif player_decision == 'd':
                if cards[0][0] != cards[1][0]:
                    print(cards[0][0], cards[1][0])
                    continue
                cards = [[card] for card in cards]
                return 'divide', cards
            return 'stick', cards

def decide_winner(player_score, dealer_score):
    if player_score == 'bust':
        if dealer_score == 'bust':
            return 'No winner. Both of you are bust'
        return 'Dealer wins. You are bust'
    elif dealer_score == 'bust':
        return 'You are the winner. Dealer is bust'
    elif dealer_score == player_score:
        return 'No winner. You have the same score'
    elif dealer_score < player_score:
        return 'You win'
    else:
        return 'You lose'

def print_cards(score, cards, player):
    hearts, diamonds, spades, clubs = chr(9829), chr(9830), chr(9824), chr(9827)
    template = """
 ___
|tt | 
| s | 
|_bb| 
"""
    print('PLAYER: {}'.format(score))
    for card in cards:
        for bit in template.splitlines():
            if bit == 't' or bit == 'b':
                print(card[:2].upper(), end='')
            elif bit == 's':
                if 'hearts' in card:
                    print(hearts, end='')
                elif 'diamonds' in card:
                    print(diamonds, end='')
                elif 'spades' in card:
                    print(spades, end='')
                else:
                    print(clubs, end='')
            else:
                print(bit, end='')
            print()
                
def play_blackjack():
    
    deck, deck_dict = make_deck()
    cards, dealer = hand(deck), hand(deck, computer = True)
    while True:
        print(cards)
        player_score = score(cards, deck_dict)
        if player_score == 'bust':
            print('you are bust.')
            break
        player_decision, cards = turn(cards, deck, deck_dict, player_score)
        if player_decision == 'stick':
            print('player sticks')
            break
        elif player_decision == 'divide':
            new_hands = {}
            for single_hand in cards:
                while True:
                    print(single_hand)
                    player_score = score(single_hand, deck_dict)
                    if player_score == 'bust':
                        print('you are bust.')
#                         new_hands[player_score] = single_hand
                        break
                    player_decision, cards = turn(single_hand, deck, deck_dict, player_score)
                    if player_decision == 'stick':
                        print('player sticks')
                        new_hands[player_score] = single_hand
                        break
            key = sorted(new_hands.keys(), key=lambda x: (x == 'bust', x))[-1]
            player_score, cards = key, new_hands[key]          
            break
    while True:
        dealer_score = score(dealer, deck_dict)
        if dealer_score == 'bust':
            print('you win. computer bust')
            break
        computer_decision, dealer = turn(dealer, deck, deck_dict, dealer_score, computer = True)
        if computer_decision == 'stick':
            print('computer sticks')
            break
    print(decide_winner(player_score, dealer_score))
    return cards, dealer, player_score, dealer_score
#     return cards, player_score

    
print(play_blackjack())
    