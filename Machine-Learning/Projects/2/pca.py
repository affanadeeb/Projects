import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_feather('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\word-embeddings.feather')
X = np.stack(df['vit'].values)  

# PCA Class Definition
class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.components = np.zeros((0, 0)) if n_components > 0 else None
        self.mean = np.zeros((0,)) if n_components > 0 else None

    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean # Centering the data by subtracting the mean
        covariance_matrix = np.cov(X_centered, rowvar=False)  # covariance matrix
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix) # Computing eigenvalues and vectors
        sorted_indices = np.argsort(eigenvalues)[::-1] # Sorting the in descending order
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        # Selecting the top n_components eigenvectors
        self.components = eigenvectors[:, :self.n_components]

    def transform(self, X):
        X_centered = X - self.mean # Centering the data by subtracting the mean
        return np.dot(X_centered, self.components)
    
    def inverse_transform(self, X_transformed):
        return np.dot(X_transformed, self.components.T) + self.mean

    def checkPCA(self, X):
        X_transformed = self.transform(X)
        X_reconstructed = self.inverse_transform(X_transformed)
        reconstruction_error = np.mean(np.square(X - X_reconstructed))
        print(f"Reconstruction error: {reconstruction_error}")
        return X_transformed.shape[1] == self.n_components and reconstruction_error < 0.04

# Applying PCA and Dimensionality Reduction
# Initialize PCA for 2 and 3 components
pca_2 = PCA(n_components=2)
pca_3 = PCA(n_components=3)

# Fitting and transforming the data (5.2)
pca_2.fit(X)
X_2D = pca_2.transform(X)

pca_3.fit(X)
X_3D = pca_3.transform(X)

# Step 4: Checking PCA functionality (5.2)
print("PCA for 2D check:", pca_2.checkPCA(X))  # Should return True
print("PCA for 3D check:", pca_3.checkPCA(X))  # Should return True

# 2D
plt.figure(figsize=(7, 5))
plt.scatter(X_2D[:, 0], X_2D[:, 1], alpha=0.7)
plt.title('2D PCA Projection')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# 3D 
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_3D[:, 0], X_3D[:, 1], X_3D[:, 2], color='lightcoral', alpha=0.7)
ax.set_title('3D PCA Projection')
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')

plt.show()

# THere are 4 to 6 clusters form the 2d and 3d plots

#  inverse transform
X_reconstructed_2D = pca_2.inverse_transform(X_2D)
X_reconstructed_3D = pca_3.inverse_transform(X_3D)

print("Original data shape:", X.shape)
print("Reconstructed 2D data shape:", X_reconstructed_2D.shape)
print("Reconstructed 3D data shape:", X_reconstructed_3D.shape)

# Calculating and printing reconstruction errors
reconstruction_error_2D = np.mean(np.square(X - X_reconstructed_2D))
reconstruction_error_3D = np.mean(np.square(X - X_reconstructed_3D))

print(f"2D Reconstruction error: {reconstruction_error_2D}")
print(f"3D Reconstruction error: {reconstruction_error_3D}")