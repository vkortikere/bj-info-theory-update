import random
import numpy as np

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def value(self):
        if self.rank == 1:
            return 11
        elif self.rank >= 10:
            return 10
        else:
            return self.rank
    
    def __repr__(self):
        rank_names = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        rank_str = rank_names.get(self.rank, str(self.rank))
        return f"{rank_str}{self.suit[0]}"

class Deck:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        self.dealt_cards = []
        self.reset()
    
    def reset(self):
        self.cards = []
        self.dealt_cards = []
        for _ in range(self.num_decks):
            for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
                for rank in range(1, 14):
                    self.cards.append(Card(rank, suit))
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) < 52:
            self.reset()
        card = self.cards.pop()
        self.dealt_cards.append(card)
        return card
    
    def cards_remaining(self):
        return len(self.cards)
    
    def get_composition(self):
        composition = {}
        for card in self.cards:
            val = min(card.rank, 10)
            composition[val] = composition.get(val, 0) + 1
        return composition

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def value(self):
        total = sum(card.value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 1)
        
        while total > 21 and num_aces > 0:
            total -= 10
            num_aces -= 1
        
        return total
    
    def is_soft(self):
        total = sum(card.value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 1)
        return num_aces > 0 and total <= 21
    
    def is_pair(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.value() == 21
    
    def __repr__(self):
        return f"Hand({[str(c) for c in self.cards]}, value={self.value()})"

class BlackjackGame:
    def __init__(self, num_decks=6, strategy=None):
        self.num_decks = num_decks
        self.deck = Deck(num_decks)
        self.strategy = strategy
    
    def play_hand(self, bet=1.0):
        player = Hand()
        dealer = Hand()
        
        player.add_card(self.deck.deal())
        dealer.add_card(self.deck.deal())
        player.add_card(self.deck.deal())
        dealer_hole_card = self.deck.deal()
        
        if player.is_blackjack():
            dealer.add_card(dealer_hole_card)
            if dealer.is_blackjack():
                return 0.0
            else:
                return bet * 1.5
        
        while player.value() < 21:
            if self.strategy is None:
                action = 'S' if player.value() >= 17 else 'H'
            else:
                action = self.strategy.get_action(player, dealer.cards[0])
            
            if action == 'S':
                break
            elif action == 'H':
                player.add_card(self.deck.deal())
            elif action == 'D':
                player.add_card(self.deck.deal())
                bet *= 2
                break
            elif action == 'P':
                break
        
        if player.value() > 21:
            return -bet
        
        dealer.add_card(dealer_hole_card)
        while dealer.value() < 17:
            dealer.add_card(self.deck.deal())
        
        if dealer.value() > 21:
            return bet
        elif player.value() > dealer.value():
            return bet
        elif player.value() < dealer.value():
            return -bet
        else:
            return 0.0