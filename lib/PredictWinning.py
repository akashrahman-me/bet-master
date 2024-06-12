import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import json

class PredictWinning():
    def __init__(self, data):
        self.data = data
        self.model = RandomForestRegressor(n_estimators=500, random_state=42)
        self.df = None
        self.X = None
        self.y = None

    def load_data(self):
        winning_number = [item['winning_number'] for item in self.data]
        total_coins = [item['total_coins'] for item in self.data]
        total_winned_coins = [item['total_winned_coins'] for item in self.data]

        data_dict = {
            "Winning Number": winning_number,
            "Total Coins": total_coins,
            "Total Winned Coins": total_winned_coins 
        }

        self.df = pd.DataFrame(data_dict)

    def preprocess_data(self):
        self.df["MA_5"] = self.df["Winning Number"].rolling(window=5).mean().shift(1)
        self.df = self.df.dropna()
        self.X = self.df.drop(columns=["Winning Number"])
        self.y = self.df["Winning Number"]

    def train_model(self):
        self.model.fit(self.X, self.y)
        y_train_pred = self.model.predict(self.X)
        mse_train = mean_squared_error(self.y, y_train_pred)
        return mse_train

    def predict_next_winning_number(self):
        last_row_features = self.X.iloc[-1].to_frame().T
        next_winning_number = self.model.predict(last_row_features)
        return next_winning_number[0]

    def run(self):

        if len(self.data) < 10:
            return 0.00, 1.00 

        self.load_data()
        self.preprocess_data()
        mse_train = self.train_model()
        next_winning_number = self.predict_next_winning_number()
        print(f"\nMSE: {mse_train:.2f}, Winning: {next_winning_number:.2f} \n")
        return mse_train, next_winning_number

# Exmaple usage
if __name__ == "__main__":
    with open('statistics.json', 'r') as f:
        data = json.load(f)
    predictor = PredictWinning(data)
    mse, winning_number = predictor.run()
    print("Train MSE:", mse)
    print("Predicted Next Winning Number:", winning_number)