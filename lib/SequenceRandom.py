import time
import random
import json

class SequenceRandom:
    def __init__(self, seed=0):
        self.state = seed

        with open ('.recharge/data-collect.json', 'r') as f:
            data = json.load(f)
        self.numbers = data
        
    def next_number(self):
        get_next = self.numbers[self.state]
        self.state = (self.state + 1) % len(self.numbers)
        return get_next
