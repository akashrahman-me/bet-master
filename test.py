import json

with open("data-collect.json", 'r') as f:
    data = json.load(f)

print(len(data))