import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json
import numpy as np
from scipy.interpolate import make_interp_spline

class RealTimePlot:
    def __init__(self, json_file, interval=1000):
        self.json_file = json_file
        self.interval = interval
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.line, = self.ax.plot([], [], linestyle="-", color='b')
        self.scatter, = self.ax.plot([], [], 'o', color='b', markersize=4)  # Adjusting marker size
        self.annotations = []
        self.setup_plot()
        
    def setup_plot(self):
        self.ax.set_title("Winning Number Plot")
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Winning Number")
        self.ax.grid(True, which='both', axis="y", linestyle='--', linewidth=0.7)

    def load_data(self):
        with open(self.json_file) as f:
            data = json.load(f)
        winning_number = [item["winning_number"] for item in data]
        return winning_number[-40:]

    def update(self, frame):
        winning_number = self.load_data()
        x = np.arange(len(winning_number))
        
        # Smooth the data
        if len(winning_number) > 3:  # Ensure there are enough points to interpolate
            x_smooth = np.linspace(x.min(), x.max(), 300)
            spl = make_interp_spline(x, winning_number, k=1)
            y_smooth = spl(x_smooth)
            self.line.set_data(x_smooth, y_smooth)
        else:
            self.line.set_data(x, winning_number)
        
        # Update scatter plot with original points
        self.scatter.set_data(x, winning_number)
        
        # Remove old annotations
        for annotation in self.annotations:
            annotation.remove()
        self.annotations.clear()

        # Add new annotations
        for i, (xi, yi) in enumerate(zip(x, winning_number)):
            annotation = self.ax.annotate(f'{yi}', (xi, yi), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='r')
            self.annotations.append(annotation)
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_ylim(0, max(winning_number) + 1)  # Ensure y-axis starts at 0
        self.ax.yaxis.set_ticks(np.arange(0, max(winning_number) + 2, 1))  # Set y-axis ticks
        return self.line, self.scatter

    def run(self):
        ani = FuncAnimation(self.fig, self.update, interval=self.interval, cache_frame_data=False)
        plt.show()

if __name__ == "__main__":
    plot = RealTimePlot("statistics.json")
    plot.run()
