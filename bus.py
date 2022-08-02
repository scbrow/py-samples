from deck_of_cards import deck_of_cards
import random

deck = deck_of_cards.DeckOfCards()
double = False
totals = 0
single_totals = 0
single_evens = 0
ride_total = 0
evens = 0
games = 0

num_sim = 10000

while games < num_sim:
    deck.reset_deck()
    if double:
        deck.add_deck()
    deck.shuffle_deck()
    bus = [0, 0, 0, 0, 0, 0, 0]
    for a in range(7):
        bus[a] = deck.give_first_card()
    j = 0
    while j < 7:
        old = bus[j]
        bus[j] = deck.give_first_card()
        ride_total += 1
        if bus[j].rank == old.rank:
            evens += 1
        if (old.rank < 7 and bus[j].rank > old.rank) or (old.rank > 7 and bus[j].rank < old.rank):
            j += 1
            continue
        if old.rank == 7:
            rand = random.uniform(0, 1)
            if (rand >= 0.5 and bus[j].rank > old.rank) or (rand < 0.5 and bus[j].rank < old.rank):
                j += 1
                continue
        j = 0
        if len(deck.deck) == 7:
            deck.take_card(deck_of_cards.Card((0, 15)))
        if len(deck.deck) < 7:
            deck.reset_deck()
            if double:
                deck.add_deck()
            deck.shuffle_deck()
            for a in range(7):
                bus[a] = deck.give_first_card()
    totals += ride_total
    ride_total = 0
    games += 1
    if games == num_sim and not double:
        double = True
        single_avg = totals/games
        single_evens = evens
        evens = 0
        games = 0
        totals = 0
print(f'Single Average: {single_avg}')
print(f'Double Average: {totals/games}')
print(f'Single Evens/Game: {single_evens/num_sim}')
print(f'Double Evens/Game: {evens/num_sim}')
