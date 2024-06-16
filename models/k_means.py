import numpy as np
import math

class KMeans:

    def __init__(self, k = 2) -> None:
        self.k = k
        self.centroids = None
        self.clusters = None
    
    def transform(self, x):
        return (x - self.x_mean) / self.x_std
    
    def normalize_data(self, x):
        self.x_std = np.std(x, axis=0)
        self.x_std[self.x_std == 0] = 1
        self.x_mean = np.mean(x, axis=0)
        return self.transform(x)

    def get_random_centroids(self, data):
        self.centroids = data[np.random.choice(data.shape[0], self.k, replace = False)]
    
    def group_data_per_clusters(self, data):
        clusters = []
        for d in data:
            distances = [math.dist(d, c) for c in self.centroids]
            clusters.append(np.argmin(distances))
        self.clusters = np.array(clusters)

    def update_centroids(self, data):
        self.centroids =  np.array([data[self.clusters == i].mean(axis=0) for i in range(self.k)])

    def error(self, data):
        sum = 0
        for i in range(self.k):
            sum += np.sum((data[self.clusters == i] - self.centroids[i])**2)
        return sum

    def train(self, data):
        self.get_random_centroids(data)
        
        while True:
            self.group_data_per_clusters(data)
            
            old_centroids = self.centroids
            self.update_centroids(data)
            print(self.centroids)
            self.error_ = self.error(data)
            print(f"ERROR: {self.error_}")
            if np.all(self.centroids == old_centroids):
                break