import time
import random
import json

class SequenceRandom:
    def __init__(self, seed):
        self.state = seed

        with open ('data-collect.json', 'r') as f:
            data = json.load(f)

        # data = [item['winning_number'] for item in data]
        self.numbers = data
        
    def next_number(self):
        get_next = self.numbers[self.state]
        self.state = (self.state + 1) % len(self.numbers)
        return get_next
