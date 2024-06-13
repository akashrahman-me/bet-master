from lib.SequenceRandom import SequenceRandom
from lib.CaptureWinnings import CaptureWinnings
from lib.StatusExtractor import StatusExtractor

class NumberPredictionGame:
    def __init__(self):
        self.coins = 1000
        self.board = 100
        self.sequence = SequenceRandom()
        self.capture_winnings = CaptureWinnings()
        self.status_extractor = StatusExtractor()

    def step(self, prediction):
        # x = self.sequence.next_number()
        # winning_number = x['winning_number']
        # total_players = x['total_players']
        # total_coins = x['total_coins']
        # total_winned_coins = x['total_winned_coins']

        # status = {
        #     "players": total_players,
        #     "bets": total_coins,
        #     "winnings": total_winned_coins
        # }
        winning_number = self.capture_winnings.run()
        status = self.status_extractor.run()
        reward = 0
        
        if prediction <= winning_number:
            reward = 0 if prediction <= 1 else (prediction * self.board) - self.board
            self.coins += reward
        else:
            reward = -self.board
            self.coins -= self.board
        
        return reward, self.coins, {
            "winning_number": winning_number,
            "total_players": status['players'],
            "total_coins": status['bets'],
            "total_winned_coins": status['winnings']
        }

    def reset(self):
        self.coins = 500
        return self.coins
