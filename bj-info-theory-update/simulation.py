import numpy as np
import pandas as pd
from tqdm import tqdm
from .blackjack import BlackjackGame
from .strategy import BasicStrategy
from .counting import HiLoCounter, KOCounter, OmegaIICounter

class Simulator:
    def __init__(self, num_decks=6, counter_type='hilo'):
        self.num_decks = num_decks
        self.strategy = BasicStrategy()
        self.counter_type = counter_type
        self.reset_counter()
    
    def reset_counter(self):
        if self.counter_type == 'hilo':
            self.counter = HiLoCounter()
        elif self.counter_type == 'ko':
            self.counter = KOCounter()
        elif self.counter_type == 'omega':
            self.counter = OmegaIICounter()
        else:
            raise ValueError(f"Unknown counter type: {self.counter_type}")
    
    def simulate(self, num_hands=100000):
        game = BlackjackGame(self.num_decks, self.strategy)
        results = []
        
        for i in tqdm(range(num_hands), desc=f"Simulating {self.counter_type}"):
            if game.deck.cards_remaining() < 52:
                game.deck.reset()
                self.counter.reset()
            
            initial_count = self.counter.running_count
            initial_cards_seen = self.counter.cards_seen
            
            dealt_cards_before = len(game.deck.dealt_cards)
            result = game.play_hand()
            dealt_cards_after = len(game.deck.dealt_cards)
            
            new_cards = game.deck.dealt_cards[dealt_cards_before:dealt_cards_after]
            for card in new_cards:
                self.counter.update(card)
            
            true_count = self.counter.get_true_count(self.num_decks)
            
            results.append({
                'hand': i,
                'result': result,
                'true_count': true_count,
                'running_count': self.counter.running_count,
                'cards_seen': self.counter.cards_seen,
                'cards_remaining': game.deck.cards_remaining()
            })
        
        return pd.DataFrame(results)
    
    def compare_systems(self, num_hands=50000):
        systems = ['hilo', 'ko', 'omega']
        all_results = {}
        
        for system in systems:
            self.counter_type = system
            self.reset_counter()
            df = self.simulate(num_hands)
            all_results[system] = df
        
        return all_results