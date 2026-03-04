class CardCounter:
    def __init__(self):
        self.running_count = 0
        self.cards_seen = 0
    
    def reset(self):
        self.running_count = 0
        self.cards_seen = 0
    
    def update(self, card):
        raise NotImplementedError
    
    def get_true_count(self, num_decks=6):
        decks_remaining = max((num_decks * 52 - self.cards_seen) / 52, 0.5)
        return self.running_count / decks_remaining
    
    def get_advantage(self, num_decks=6):
        tc = self.get_true_count(num_decks)
        return -0.005 + 0.005 * tc

class HiLoCounter(CardCounter):
    def update(self, card):
        rank = card.rank
        if 2 <= rank <= 6:
            self.running_count += 1
        elif rank >= 10 or rank == 1:
            self.running_count -= 1
        self.cards_seen += 1

class KOCounter(CardCounter):
    def update(self, card):
        rank = card.rank
        if 2 <= rank <= 7:
            self.running_count += 1
        elif rank >= 10 or rank == 1:
            self.running_count -= 1
        self.cards_seen += 1

class OmegaIICounter(CardCounter):
    def update(self, card):
        rank = card.rank
        if rank in [2, 3, 7]:
            self.running_count += 1
        elif rank in [4, 5, 6]:
            self.running_count += 2
        elif rank == 9:
            self.running_count -= 1
        elif rank >= 10 or rank == 1:
            self.running_count -= 2
        self.cards_seen += 1
    
    def get_true_count(self, num_decks=6):
        decks_remaining = max((num_decks * 52 - self.cards_seen) / 52, 0.5)
        return self.running_count / (2 * decks_remaining)