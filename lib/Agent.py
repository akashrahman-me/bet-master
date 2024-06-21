from lib.NumberPredictionGame import NumberPredictionGame
from lib.PredictWinning import PredictWinning
import re
import json
import time
from lib.CaptureWinnings import CaptureWinnings
import threading
from utils.touch_screen import touch_screen

class Agent:
    def __init__(self):
        self.step = 0
        self.game = NumberPredictionGame()
        self.statistics = []
        self.capture_winnings = CaptureWinnings()

    def prediction(self):    
        pred_data = self.statistics if len(self.statistics) > 500 else self.statistics[-500:]

        preper_train = [{
            'winning_number': item['winning_number'],
            'total_coins': item['total_coins'],
            'total_winned_coins': item['total_winned_coins']
        } for item in pred_data]

        if len(preper_train) <= 2:
            return 1

        with open ('storage/500_match.json', 'r') as f:
            match_500 = json.load(f)
            match_500 = [{
                'winning_number': item['winning_number'],
                'total_coins': item['total_coins'],
                'total_winned_coins': item['total_winned_coins']
            } for item in match_500]

        trainable_data = match_500 + preper_train

        predict = PredictWinning(pred_data)
        mse, winning_number = predict.run()
        if mse <= 5 and winning_number >= 2:
            return winning_number
        return 1

    def run(self):

        while True:

            if self.step > 458:
                break

            action = self.prediction()
            
            print(f"Step: {self.step}, Prediction: {action:.2f}")

            # Place bet.
            # if action > 1:
            #     def bet_placing_macanisum():
            #         try:
            #             time.sleep(3)
            #             # Here <click the place button>
            #             # touch_screen(290, 1350) # Place a Bet

            #             self.capture_winnings.run(target=action)

            #             # Here click the up button
            #             # touch_screen(800, 1350) #Take Winning

            #         except Exception as e:
            #             print(e)

            #     threading.Thread(target=bet_placing_macanisum).start()


            reward, coins, status = self.game.step(action)
            print(f"Reward: {reward:.2f}, Coins: {coins:.2f}\n")

            if self.step % 600 == 0:
                time.sleep(3)

            try:
                self.statistics.append({
                    "prediction_winning_number": round(action, 2),
                    "winning_number": round(status['winning_number'], 2),
                    "reward": round(reward, 2),
                    "coins": round(coins, 2),
                    "total_coins": round(status['total_coins'], 2),
                    "total_winned_coins": round(status['total_winned_coins'], 2)
                })

                with open('statistics.json', 'w') as f:
                    json.dump(self.statistics, f, indent=4)

            except Exception as e:
                print(e)


            self.step += 1

            # Stopping condition (example: stop if coins fall below a certain threshold)
            if coins <= 0:
                print(f"Game over at step {self.step}, final coins: {coins}")
                break

if __name__ == "__main__":
    agent = Agent()
    agent.run()