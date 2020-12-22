#!/env/python3

text_file = open("Day_22/input", "r")
lines = [x.strip() for x in text_file.readlines()]

# Part 01

empty_line = lines.index('')
deck_1 = [int(x) for x in lines[1:empty_line]]
deck_2 = [int(x) for x in lines[empty_line+2:]]

while deck_1 and deck_2:
    card_1 = deck_1.pop(0)
    card_2 = deck_2.pop(0)
    if card_1 > card_2:
        deck_1.append(card_1)
        deck_1.append(card_2)
    else:
        deck_2.append(card_2)
        deck_2.append(card_1)

# Calculate winners score
winning_deck = deck_2
if deck_1:
    winning_deck = deck_1

player_score = 0
card_value = 1
for card in winning_deck[::-1]:
    card_score = card_value * card
    player_score += card_score
    card_value += 1

print("Part 01: Player score = {}".format(player_score))


# Part 02
game = 0


def play_game(deck_1: list, deck_2: list) -> (int, list):
    global game
    game += 1
    sub_game = game
    deck_record = []

    play_round = 0
    while deck_1 and deck_2:
        play_round += 1

        # check for previous deck and record the current deck
        deck_img = str(deck_1) + "|" + str(deck_2)
        if deck_img in deck_record:
            return (1, deck_1)
            break
        deck_record.append(deck_img)

        card_1 = deck_1.pop(0)
        card_2 = deck_2.pop(0)

        winner: int
        if len(deck_1) >= card_1 and len(deck_2) >= card_2:
            # Play recursive sub game
            winner, _ = play_game(deck_1[:card_1], deck_2[:card_2])
        elif card_1 > card_2:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            deck_1.append(card_1)
            deck_1.append(card_2)
        elif winner == 2:
            deck_2.append(card_2)
            deck_2.append(card_1)
        else:
            print("Nobody won?")

    if deck_1:
        return (1, deck_1)
    else:
        return (2, deck_2)


deck_1 = [int(x) for x in lines[1:empty_line]]
deck_2 = [int(x) for x in lines[empty_line+2:]]
winner, winning_deck = play_game(deck_1, deck_2)

player_score = 0
card_value = 1
for card in winning_deck[::-1]:
    card_score = card_value * card
    player_score += card_score
    card_value += 1

print("Part 02: Player score = {}".format(player_score))
