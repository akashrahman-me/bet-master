import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import time

class RealTimePlot:
    def __init__(self, json_file, interval=1000):
        self.json_file = json_file
        self.interval = interval
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.line, = self.ax.plot([], [], marker='o', linestyle='-', color='b', markersize=0)
        self.ax.set_title('Line Chart of Provided Data')
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Value')
        self.ax.grid(True, color="blue", linestyle='--')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['bottom'].set_color('none')
        self.ax.spines['left'].set_color('none')

    def get_data(self):
        attempts = 0
        while attempts < 5:  # Retry up to 5 times
            try:
                with open(self.json_file, 'r') as f:
                    data = json.load(f)
                    winning_numers = [item['winning_number'] for item in data]
                    if len(winning_numers) > 100:
                        winning_numers = winning_numers[-100:]
                    return winning_numers
            except json.JSONDecodeError:
                time.sleep(0.1)  # Wait a bit before retrying
                attempts += 1
        return []  # Return an empty list if all attempts fail

    def update(self, frame):
        data = self.get_data()
        self.line.set_data(range(len(data)), data)
        self.ax.relim()
        self.ax.autoscale_view()
        return self.line,

    def run(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=self.interval, cache_frame_data=False)
        plt.show()

# Usage
plot = RealTimePlot('data-collect.json')
plot.run()
