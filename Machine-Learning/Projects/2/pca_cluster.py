import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.stats import multivariate_normal
from scipy.special import logsumexp

# PCA Class (I can direclt use from pca_class import PCA which is stored in models folder
# but i am getting errors that's why i have written in this way)
class PCA:
    def __init__(self, n_components=None):
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.explained_variance = None

    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean  # Centering the data by subtracting the mean
        covariance_matrix = np.cov(X_centered, rowvar=False)  # Covariance matrix
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)  # Eigenvalues and vectors
        sorted_indices = np.argsort(eigenvalues)[::-1]  # Sorting in descending order
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        self.explained_variance = eigenvalues / np.sum(eigenvalues)
        if self.n_components is None:
            self.n_components = len(eigenvalues)
        # Selecting the top n_components eigenvectors
        self.components = eigenvectors[:, :self.n_components]

    def transform(self, X):
        X_centered = X - self.mean  # Centering the data
        return np.dot(X_centered, self.components)

# Function to create a scree plot
def plot_scree(pca):
    plt.figure(figsize=(8, 6))
    plt.plot(np.arange(1, len(pca.explained_variance) + 1), pca.explained_variance, marker='o', linestyle='--')
    plt.xlabel('Number of Components')
    plt.ylabel('Explained Variance Ratio')
    plt.title('Scree Plot')
    plt.grid(True)
    plt.show()

# K-means clustering 
def kmeans(X, K, max_iters=100):
    np.random.seed(42)
    centroids = X[np.random.choice(range(len(X)), K, replace=False)]
    
    for _ in range(max_iters):
        distances = np.array([np.linalg.norm(X - centroid, axis=1) for centroid in centroids])
        labels = np.argmin(distances, axis=0)
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(K)])
        
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    return centroids, labels

# Elbow Method
def elbow_method(X, max_clusters=10):
    distortions = []
    K = range(1, max_clusters + 1)
    for k in K:
        centroids, labels = kmeans(X, k)
        distortions.append(sum(np.min(cdist(X, centroids, 'euclidean'), axis=1)) / X.shape[0])
    
    # Plotting the Elbow Plot
    plt.figure(figsize=(8, 6))
    plt.plot(K, distortions, marker='o', linestyle='--')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Distortion')
    plt.title('Elbow Method for Optimal K')
    plt.grid(True)
    plt.show()





class GMM:
    def __init__(self, n_components, max_iter=100, tol=1e-3, reg_covar=1e-6):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
        self.reg_covar = reg_covar
        self.weights = None
        self.means = None
        self.covariances = None

    def initialize(self, X):
        n_samples, n_features = X.shape
        
        self.weights = np.full(self.n_components, 1 / self.n_components)
        self.means = X[np.random.choice(n_samples, self.n_components, replace=False)]
        
        self.covariances = []
        for _ in range(self.n_components):
            covariance_matrix = np.cov(X.T) + self.reg_covar * np.eye(n_features)
            self.covariances.append(covariance_matrix)


    def e_step(self, X):
        n_samples = X.shape[0]
        log_resp = np.zeros((n_samples, self.n_components))
        for k in range(self.n_components):
            log_resp[:, k] = np.log(self.weights[k] + 1e-300) + self._log_multivariate_normal_pdf(X, self.means[k], self.covariances[k])
        log_resp_norm = logsumexp(log_resp, axis=1)
        log_resp -= log_resp_norm[:, np.newaxis]
        return np.exp(log_resp)

    def m_step(self, X, responsibilities):
        n_samples, n_features = X.shape
        self.weights = responsibilities.sum(axis=0) / n_samples
        self.weights = np.clip(self.weights, 1e-10, 1)
        self.weights /= self.weights.sum()
        for k in range(self.n_components):
            resp_k = responsibilities[:, k]
            resp_sum = resp_k.sum()
            if resp_sum > 0:
                self.means[k] = (X * resp_k[:, np.newaxis]).sum(axis=0) / resp_sum
                diff = X - self.means[k]
                self.covariances[k] = np.dot(resp_k * diff.T, diff) / resp_sum + self.reg_covar * np.eye(n_features)
            else:
                self.means[k] = X.mean(axis=0)
                self.covariances[k] = np.cov(X.T) + self.reg_covar * np.eye(n_features)

    def fit(self, X):
        self.initialize(X)
        prev_log_likelihood = -np.inf
        for _ in range(self.max_iter):
            responsibilities = self.e_step(X)
            self.m_step(X, responsibilities)
            log_likelihood = self.log_likelihood(X)
            if np.isfinite(log_likelihood) and np.abs(log_likelihood - prev_log_likelihood) < self.tol:
                break
            prev_log_likelihood = log_likelihood

    def _log_multivariate_normal_pdf(self, X, mean, cov):
        n_samples, n_features = X.shape
        diff = X - mean
        try:
            chol = np.linalg.cholesky(cov)
            log_det = 2 * np.sum(np.log(np.diag(chol)))
            quad_form = np.sum(np.linalg.solve(chol, diff.T)**2, axis=0)
        except np.linalg.LinAlgError:
            return -np.inf * np.ones(n_samples)
        return -0.5 * (n_features * np.log(2 * np.pi) + log_det + quad_form)

    def log_likelihood(self, X):
        n_samples = X.shape[0]
        log_likelihood = np.zeros((n_samples, self.n_components))
        
        for k in range(self.n_components):
            weight_term = np.log(self.weights[k] + 1e-300)
            pdf_term = self._log_multivariate_normal_pdf(X, self.means[k], self.covariances[k])
            log_likelihood[:, k] = weight_term + pdf_term
        
        summed_log_likelihood = logsumexp(log_likelihood, axis=1)
        return np.sum(summed_log_likelihood)


    def bic(self, X):
        n_samples, n_features = X.shape
        n_parameters = self.n_components * (n_features + n_features * (n_features + 1) / 2) + self.n_components - 1
        log_likelihood = self.log_likelihood(X)
        bic_value = -2 * log_likelihood + n_parameters * np.log(n_samples)
        return bic_value

    def aic(self, X):
        n_samples, n_features = X.shape
        n_parameters = self.n_components * (n_features + n_features * (n_features + 1) / 2) + self.n_components - 1
        log_likelihood = self.log_likelihood(X)
        aic_value = -2 * log_likelihood + 2 * n_parameters
        return aic_value


def find_optimal_clusters(X, max_clusters=10):
    bic_scores = []
    aic_scores = []
    for n_components in range(1, max_clusters + 1):
        try:
            gmm = GMM(n_components=n_components)
            gmm.fit(X)
            bic_scores.append(gmm.bic(X))
            aic_scores.append(gmm.aic(X))
        except Exception as e:
            print(f"Error fitting GMM with {n_components} components: {e}")
            bic_scores.append(np.inf)
            aic_scores.append(np.inf)
    
    optimal_clusters_bic = np.argmin(bic_scores) + 1
    optimal_clusters_aic = np.argmin(aic_scores) + 1
    
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, max_clusters + 1), bic_scores, marker='o', label='BIC')
    plt.plot(range(1, max_clusters + 1), aic_scores, marker='s', label='AIC')
    plt.xlabel('Number of clusters')
    plt.ylabel('Score')
    plt.title('BIC and AIC Scores vs. Number of Clusters')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return optimal_clusters_bic, optimal_clusters_aic

# Main script
if __name__ == "__main__":
    df = pd.read_feather('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\word-embeddings.feather')
    X = np.stack(df['vit'].values)  

    # 6.1 is in Kmeans.py 
    
    # Apply PCA
    pca = PCA(n_components=None)  # Initially, we don't know the optimal number of components
    pca.fit(X)
    
    # Scree plot to identify optimal number of dimensions
    plot_scree(pca)
    
    # Reducing the dataset to the first 3 components as determined from the scree plot
    n_components = 3
    reduced_X = pca.transform(X)[:, :n_components]
    print("Reduced data shape:", reduced_X.shape)
    
    # Apply Elbow Method to determine the optimal number of clusters
    elbow_method(reduced_X, max_clusters=10)
    
    #optimal number of clusters is 4 (from elbow plot)
    k_optimal = 4
    centroids, labels = kmeans(reduced_X, k_optimal)
    
    # Plot the reduced dataset with clusters (using first two dimensions for visualization)
    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_X[:, 0], reduced_X[:, 1], c=labels, cmap='viridis', s=50)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200)
    plt.title(f'K-Means Clustering (K={k_optimal}) on Reduced Dataset')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.grid(True)
    plt.show()


    # 6.3 is done in gmm.py only

    #Below is 6.4
    kgmm_bic, kgmm_aic = find_optimal_clusters(reduced_X, max_clusters=10)
    print(f"Optimal number of clusters (BIC): {kgmm_bic}")
    print(f"Optimal number of clusters (AIC): {kgmm_aic}")
    
    # Applying GMM with kgmm_bic==K_gmm3==4
    gmm = GMM(n_components=kgmm_bic)
    gmm.fit(reduced_X)
    
    # Assign cluster labels
    responsibilities = gmm.e_step(reduced_X)
    labels = np.argmax(responsibilities, axis=1)
    
    # Plotting the reduced dataset with GMM clusters (first two dimensions)
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(reduced_X[:, 0], reduced_X[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
    
    # Plotting the means of the Gaussian components (first two dimensions)
    for i, mean in enumerate(gmm.means):
        plt.scatter(mean[0], mean[1], c='red', marker='x', s=200, linewidths=3)
        
    plt.colorbar(scatter)
    plt.title(f'GMM Clustering (K={kgmm_bic}) on Reduced Dataset')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.grid(True)
    plt.show()