from lib.NumberPredictionGame import NumberPredictionGame
from lib.PredictWinning import PredictWinning
from lib.ScreenCapture import ScreenCapture
from lib.CustomRandomGenerator import CustomRandomGenerator
import easyocr
import re
import json
import random
import pyautogui

class Agent:
    def __init__(self):
        self.statistics = []
        self.reader = easyocr.Reader(['en'])

    def find_image_center(self, image_path):
        while True:
            try:
                location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
                if location:
                    x, y = location
                    return (x, y)
                else:
                    continue
            except pyautogui.ImageNotFoundException:
                continue

    def extract_digits(self, text):
        # Extract only digits and spaces
        digits_text = re.findall(r'\d+\.\d+|\d+', text)
        return digits_text

    def find_consistent_center(self, image_path, required_matches=5):
        last_centers = []
        while True:
            response_x_center, response_y_center = self.find_image_center(image_path)
            last_centers.append((response_x_center, response_y_center))
            if len(last_centers) > required_matches:
                last_centers.pop(0)
            if len(last_centers) == required_matches and all(center == last_centers[0] for center in last_centers):
                return last_centers[0]

    def extract_prediction(self):
        image_path = 'images/response_button.png'
        response_x_center, response_y_center = self.find_consistent_center(image_path)

        width = 350
        height = 32
        x = int(response_x_center) - 112
        y = int(response_y_center) - 60

        screen_capture = ScreenCapture(width, height, x, y)
        screenshot = screen_capture.capture_screenshot()
        screenshot = screen_capture.save_screenshot(screenshot)

        def extract_winning_number(data):
            if isinstance(data, list):
                data = " ".join(data)
            match = re.search(r"Predict next winning number: (\d+\.\d+)", data)
            if match:
                return float(match.group(1))
            else:
                print(f"No match found: {data}")
                return 1.00

        text = self.reader.readtext(screenshot, detail=0)
        return float(extract_winning_number(text))

    def write_gpt(self, text):
        coordinate = self.find_image_center("images/chatgpt_input.png")
        pyautogui.click(coordinate)
        pyautogui.write(text, interval=0.004)
        pyautogui.press('enter')

    def extract_number(self, text):
        # Use regular expression to find the number in the text
        match = re.search(r'\d+\.\d+', text)
        if match:
            return float(match.group())
        else:
            return 1.0

    def prediction(self):    
        pred_data = self.statistics
        if len(pred_data) > 500:
            pred_data = pred_data[-500:] 
        predict = PredictWinning(pred_data)
        mse, winning_number = predict.run()
        if mse < 2.25:
            return winning_number
        return 1

        # return self.extract_prediction()

    def run(self):
        game = NumberPredictionGame()
        step = 0
        self.statistics = []

        while True:
            if step >= 600:
                break

            action = self.prediction()
            print(f"Prediction: {action:.2f}")
            reward, coins, status = game.step(action)
            print(f"Reward: {reward:.2f}, Coins: {coins:.2f}\n")

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
                    json.dump(self.statistics, f)

            except Exception as e:
                print(e)

            # ChatGPT
            instr = ""
            if reward < 0:
                instr =  "It seems you're lossing the reward, please try hard to avoid lossing rewards"
            if reward == 0:
                instr = "It seems you're winning the reward, please try to win more rewards"
                
            # self.write_gpt(f"Winning number: {status['winning_number']} Total players: {status['total_players']} Total coins: {status['total_coins']} Total winned coins: {status['total_winned_coins']} Reward: {reward:.2f} Coins: {coins:.2f} {instr}")

            # # Proof typing and Enter successful
            # self.find_image_center('images/chatgpt_input.png')

            step += 1

            # Stopping condition (example: stop if coins fall below a certain threshold)
            if coins <= 0:
                print(f"Game over at step {step}, final coins: {coins}")
                break

if __name__ == "__main__":
    agent = Agent()
    agent.run()