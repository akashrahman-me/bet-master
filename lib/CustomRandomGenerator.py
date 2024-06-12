import numpy as np

class CustomRandomGenerator:
    def __init__(self, values):
        self.values = values
        self.sorted_values = sorted(values)
        self.bins, self.probabilities = self._calculate_bins_and_probabilities()

    def _calculate_bins_and_probabilities(self):
        # Automatically determine the number of bins using the Freedman-Diaconis rule
        q25, q75 = np.percentile(self.sorted_values, [25, 75])
        bin_width = 2 * (q75 - q25) * len(self.sorted_values) ** (-1/3)
        num_bins = int((max(self.sorted_values) - min(self.sorted_values)) / bin_width)

        # Calculate bin edges
        bins = np.linspace(min(self.sorted_values), max(self.sorted_values), num_bins + 1)

        # Calculate the probabilities for each bin
        probabilities = []
        for i in range(len(bins) - 1):
            count = sum(1 for x in self.sorted_values if bins[i] <= x < bins[i + 1])
            probabilities.append(count / len(self.values))

        # Ensure the last bin includes the maximum value
        probabilities[-1] += sum(1 for x in self.sorted_values if x == bins[-1]) / len(self.values)

        # Normalize probabilities to ensure they sum to 1
        probabilities = np.array(probabilities) / sum(probabilities)

        return bins, probabilities

    def custom_random(self):
        bin_choice = np.random.choice(len(self.probabilities), p=self.probabilities)
        return np.random.uniform(self.bins[bin_choice], self.bins[bin_choice + 1])

    def generate_random_numbers(self, n=60):
        return [self.custom_random() for _ in range(n)]