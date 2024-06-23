import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from lib.CustomRandomGenerator import CustomRandomGenerator
from lib.PatternMatcher import PatternMatcher
import json
import numpy as np
import random

class PredictWinning():
    def __init__(self, data):
        self.data = data
        self.data = [item['winning_number'] for item in self.data]
        self.matcher = PatternMatcher()

    def predict_next_winning_number(self):

        # insufficient data
        if len(self.data) < 6:
            return 1
        
        if sum(self.data[-6:]) <= 40:
            return 1
    
        if self.data[-1:][0] >= 14:
            return 1
        
        return 3

        return 1

    def run(self):        
        next_winning_number = self.predict_next_winning_number()
        return 1, next_winning_number