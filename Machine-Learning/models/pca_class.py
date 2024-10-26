import numpy as np

# PCA Class Definition
class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.explained_variance = None

    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean # Centering the data by subtracting the mean
        covariance_matrix = np.cov(X_centered, rowvar=False)  # covariance matrix
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix) # Computing eigenvalues and vectors
        sorted_indices = np.argsort(eigenvalues)[::-1] # Sorting the in descending order
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        self.explained_variance = eigenvalues / np.sum(eigenvalues)
        if self.n_components is None:
            self.n_components = len(eigenvalues)
        # Selecting the top n_components eigenvectors
        self.components = eigenvectors[:, :self.n_components]

    def transform(self, X):
        X_centered = X - self.mean # Centering the data by subtracting the mean
        return np.dot(X_centered, self.components)

    def checkPCA(self, X):
        X_transformed = self.transform(X) # Transforming the data
        return X_transformed.shape[1] == self.n_components # Checking if the number of dimensions is correct