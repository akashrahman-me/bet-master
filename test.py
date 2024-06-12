import json

with open ('data-collect.json', 'r') as f:
    data = json.load(f)
    data = [item['winning_number'] for item in data]

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Prepare the data for supervised learning
def create_dataset(data, n_steps=3):
    X, y = [], []
    for i in range(len(data)):
        end_ix = i + n_steps
        if end_ix > len(data)-1:
            break
        seq_x, seq_y = data[i:end_ix], data[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

# Define the number of time steps
n_steps = 3

# Create the dataset
X, y = create_dataset(data, n_steps)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestRegressor
model = RandomForestRegressor(n_estimators=500, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Predict the next number in the sequence
next_input = np.array(data[-n_steps:]).reshape(1, -1)
next_number = model.predict(next_input)

print(f"Predicted next number: {next_number[0]}")
