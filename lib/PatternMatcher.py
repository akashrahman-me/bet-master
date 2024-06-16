import numpy as np

class PatternMatcher:
    def __init__(self):
        self.dataset = []
        self.pattern = []
        self.normalized_dataset = []
        self.normalized_pattern = []
    
    def normalize_sequence(self, sequence):
        min_val = min(sequence)
        max_val = max(sequence)
        return [(x - min_val) / (max_val - min_val) for x in sequence]
    
    def calculate_similarity_score(self, segment, pattern):
        distance = np.linalg.norm(np.array(segment) - np.array(pattern))
        max_distance = np.sqrt(len(segment))  # Maximum possible distance in normalized space
        similarity = (1 - (distance / max_distance)) * 100
        return similarity
    
    def check_pattern_with_euclidean(self):
        dataset_length = len(self.dataset)
        pattern_length = len(self.pattern)
        
        # Normalize the dataset and pattern
        extended_dataset = self.dataset + self.dataset[:pattern_length-1]
        normalized_extended_dataset = self.normalize_sequence(extended_dataset)
        
        # Initialize the best similarity score
        best_similarity = 0.0
        
        # Slide over the extended normalized dataset and calculate similarity score
        for i in range(dataset_length):
            segment = normalized_extended_dataset[i:i + pattern_length]
            similarity = self.calculate_similarity_score(segment, self.normalized_pattern)
            if similarity > best_similarity:
                best_similarity = similarity
        
        return best_similarity
    
    def pattern_match(self):
        similarity_score = self.check_pattern_with_euclidean()
        return True if similarity_score > 75 else False
    
    def run(self, dataset, pattern):
        self.dataset = dataset
        self.pattern = pattern
        self.normalized_dataset = self.normalize_sequence(dataset)
        self.normalized_pattern = self.normalize_sequence(pattern)
        return self.pattern_match()