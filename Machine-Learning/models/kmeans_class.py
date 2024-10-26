import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class KMeans:
    def __init__(self, k=3, max_iters=100, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None

    def initialize_centroids(self, X):
        np.random.seed(42)
        # Use permutation to select initial centroids
        num_samples = len(X)
        shuffled_indices = np.random.permutation(num_samples)
        selected_indices = shuffled_indices[:self.k]
        self.centroids = X[selected_indices]

    def compute_distance(self, X, centroids):
        diff = X[:, np.newaxis] - centroids # diff between each point and centroids
        squared_diff = np.square(diff) # squared differences
        summed_squared_diff = np.sum(squared_diff, axis=2)
        return np.sqrt(summed_squared_diff)

    def update_centroids(self, X, labels):
        new_centroids_list = []
        # Loop over each cluster to compute its centroid
        for i in range(self.k):
            cluster_points = X[labels == i]
            new_centroid = cluster_points.mean(axis=0)
            new_centroids_list.append(new_centroid)
        return np.array(new_centroids_list)


    def fit(self, X):
        self.initialize_centroids(X)
        for _ in range(self.max_iters):
            distances = self.compute_distance(X, self.centroids)
            labels = np.argmin(distances, axis=1)
            new_centroids = self.update_centroids(X, labels)
            centroid_shift = np.abs(new_centroids - self.centroids) #Checking if centroids have converged
            if np.all(centroid_shift < self.tol):
                break
            self.centroids = new_centroids

    def predict(self, X):
        #Predicting the closest cluster for each sample in X
        distances = self.compute_distance(X, self.centroids)
        return np.argmin(distances, axis=1)

    def getCost(self, X):
        distances = self.compute_distance(X, self.centroids)
        min_distances = np.min(distances, axis=1)
        return np.sum(min_distances ** 2)