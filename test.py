import json

with open("data-collect.json", "r") as f:
    data = json.load(f)


print(len([item['winning_number'] for item in data]))