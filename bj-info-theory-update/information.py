import numpy as np
from scipy.stats import entropy

class InformationTheory:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.total_cards = num_decks * 52
    
    def initial_entropy(self):
        cards_per_rank = self.num_decks * 4
        probs = []
        for rank in range(1, 14):
            if rank >= 10:
                probs.extend([cards_per_rank / self.total_cards] * 4)
            else:
                probs.append(cards_per_rank / self.total_cards)
        return entropy(probs, base=2)
    
    def deck_entropy(self, composition):
        total = sum(composition.values())
        if total == 0:
            return 0
        probs = [count / total for count in composition.values()]
        return entropy(probs, base=2)
    
    def mutual_information(self, observed_cards, remaining_composition):
        prior_entropy = self.initial_entropy()
        posterior_entropy = self.deck_entropy(remaining_composition)
        return prior_entropy - posterior_entropy
    
    def information_from_count(self, true_count, cards_seen):
        cards_remaining = self.total_cards - cards_seen
        if cards_remaining <= 0:
            return 0
        
        high_cards_deviation = true_count * (cards_remaining / 52)
        
        total_high = self.num_decks * 20
        total_low = self.num_decks * 20
        total_neutral = self.num_decks * 12
        
        high_remaining = total_high - (cards_seen * 20 / 52) + high_cards_deviation
        low_remaining = total_low - (cards_seen * 20 / 52) - high_cards_deviation
        neutral_remaining = total_neutral - (cards_seen * 12 / 52)
        
        composition = {
            'high': max(0, high_remaining),
            'low': max(0, low_remaining),
            'neutral': max(0, neutral_remaining)
        }
        
        return self.mutual_information(cards_seen, composition)
    
    def ev_information_bound(self, mutual_info):
        return 0.015 * mutual_info - 0.005