class BasicStrategy:
    def __init__(self):
        self.hard_strategy = self._init_hard_strategy()
        self.soft_strategy = self._init_soft_strategy()
        self.pair_strategy = self._init_pair_strategy()
    
    def _init_hard_strategy(self):
        strategy = {}
        
        for total in range(5, 22):
            for dealer_up in range(2, 12):
                if total <= 8:
                    strategy[(total, dealer_up)] = 'H'
                elif total == 9:
                    strategy[(total, dealer_up)] = 'D' if 3 <= dealer_up <= 6 else 'H'
                elif total == 10:
                    strategy[(total, dealer_up)] = 'D' if dealer_up <= 9 else 'H'
                elif total == 11:
                    strategy[(total, dealer_up)] = 'D'
                elif total == 12:
                    strategy[(total, dealer_up)] = 'S' if 4 <= dealer_up <= 6 else 'H'
                elif 13 <= total <= 16:
                    strategy[(total, dealer_up)] = 'S' if dealer_up <= 6 else 'H'
                else:
                    strategy[(total, dealer_up)] = 'S'
        
        return strategy
    
    def _init_soft_strategy(self):
        strategy = {}
        
        for total in range(13, 22):
            for dealer_up in range(2, 12):
                if total <= 17:
                    strategy[(total, dealer_up)] = 'D' if 4 <= dealer_up <= 6 else 'H'
                elif total == 18:
                    if dealer_up <= 6:
                        strategy[(total, dealer_up)] = 'D'
                    elif dealer_up in [7, 8]:
                        strategy[(total, dealer_up)] = 'S'
                    else:
                        strategy[(total, dealer_up)] = 'H'
                else:
                    strategy[(total, dealer_up)] = 'S'
        
        return strategy
    
    def _init_pair_strategy(self):
        strategy = {}
        
        pairs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for pair in pairs:
            for dealer_up in range(2, 12):
                if pair == 1 or pair == 8:
                    strategy[(pair, dealer_up)] = 'P'
                elif pair == 10:
                    strategy[(pair, dealer_up)] = 'S'
                elif pair == 9:
                    strategy[(pair, dealer_up)] = 'P' if dealer_up != 7 and dealer_up <= 9 else 'S'
                elif pair == 7:
                    strategy[(pair, dealer_up)] = 'P' if dealer_up <= 7 else 'H'
                elif pair == 6:
                    strategy[(pair, dealer_up)] = 'P' if dealer_up <= 6 else 'H'
                elif pair == 5:
                    strategy[(pair, dealer_up)] = 'D' if dealer_up <= 9 else 'H'
                elif pair == 4:
                    strategy[(pair, dealer_up)] = 'P' if 5 <= dealer_up <= 6 else 'H'
                elif pair in [2, 3]:
                    strategy[(pair, dealer_up)] = 'P' if dealer_up <= 7 else 'H'
        
        return strategy
    
    def get_action(self, player_hand, dealer_upcard):
        dealer_val = min(dealer_upcard.rank, 10) if dealer_upcard.rank != 1 else 11
        
        if player_hand.is_pair():
            pair_rank = player_hand.cards[0].rank
            action = self.pair_strategy.get((pair_rank, dealer_val), 'H')
            if action == 'P':
                return 'P'
        
        if player_hand.is_soft():
            key = (player_hand.value(), dealer_val)
            return self.soft_strategy.get(key, 'S')
        else:
            key = (player_hand.value(), dealer_val)
            return self.hard_strategy.get(key, 'S')