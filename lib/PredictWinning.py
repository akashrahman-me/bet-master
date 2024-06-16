import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from lib.CustomRandomGenerator import CustomRandomGenerator
from lib.PatternMatcher import PatternMatcher
import json
import numpy as np

class PredictWinning():
    def __init__(self, data):
        self.data = data
        self.data = [item['winning_number'] for item in self.data]
        self.matcher = PatternMatcher()


    def predict_next_winning_number(self): 
        if sum(self.data[-6:]) <= 40:
            return 1
        
        # 14+
        if self.data[-1:][0] >= 14:
            return 1

        # 1, 1, 2, 1       
        if (self.matcher.run(self.data[-4:], [1, 1, 2, 1])):
            return 3
            
        # 1, 1, 1, 2
        if (self.matcher.run(self.data[-4:], [1, 1, 1, 2])):
            return 3

        # 2, 1, 2, 5, 1.5
        if (self.matcher.run(self.data[-5:], [2.19, 1.05, 2.39, 4.71, 1.65])):
            return 3
        
        return 1

    def run(self):
        if len(self.data) < 10:
            print("It's returning 0.00, 1.00 due to insufficient data")
            return 0.00, 1.00
        
        next_winning_number = self.predict_next_winning_number()
        return 1, next_winning_number