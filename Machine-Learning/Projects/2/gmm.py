import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import logsumexp
from sklearn.mixture import GaussianMixture # just for checking if sklearn thing works or not
from sklearn.manifold import TSNE

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
        self.weights = np.full(self.n_components, 1 / self.n_components)# Initializing weights to be uniform
        random_indices = np.random.choice(n_samples, self.n_components, replace=False)# Randomly selecting initial means
        self.means = X[random_indices]
        covariance_matrix = np.cov(X.T) # covariances
        identity_matrix = self.reg_covar * np.eye(n_features)
        self.covariances = [covariance_matrix + identity_matrix for _ in range(self.n_components)]

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
            log_likelihood = self.getLikelihood(X)
            if np.isfinite(log_likelihood):
                change_in_log_likelihood = np.abs(log_likelihood - prev_log_likelihood)
                if change_in_log_likelihood < self.tol:
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

    def getParams(self):
        return {
            'weights': self.weights,
            'means': self.means,
            'covariances': self.covariances
        }

    def getMembership(self, X):
        return self.e_step(X)

    def getLikelihood(self, X):
        n_samples = X.shape[0]
        log_likelihood = np.zeros((n_samples, self.n_components))
        # Computing log-likelihood for each component
        for k in range(self.n_components):
            weight_term = np.log(self.weights[k] + 1e-300)
            pdf_term = self._log_multivariate_normal_pdf(X, self.means[k], self.covariances[k])
            log_likelihood[:, k] = weight_term + pdf_term
        # computing total log-likelihood by Normalizing log-likelihood
        log_likelihood_normalized = logsumexp(log_likelihood, axis=1)
        total_log_likelihood = np.sum(log_likelihood_normalized)
        
        return total_log_likelihood


    def bic(self, X):
        n_samples, n_features = X.shape
        n_parameters = (
            self.n_components * (n_features + n_features * (n_features + 1) / 2) +
            self.n_components - 1
        )
        log_likelihood = self.getLikelihood(X)
        # Calculating BIC
        bic_value = -2 * log_likelihood + n_parameters * np.log(n_samples)
        return bic_value


    def aic(self, X):
        n_samples, n_features = X.shape
        n_parameters = (
            self.n_components * (n_features + n_features * (n_features + 1) / 2) +
            self.n_components - 1
        )
        log_likelihood = self.getLikelihood(X)
        # Calculating AIC
        aic_value = -2 * log_likelihood + 2 * n_parameters
        return aic_value


def find_optimal_clusters(X, max_clusters=10, use_sklearn=False):
    bic_scores = []
    aic_scores = []
    for n_components in range(1, max_clusters + 1):
        try:
            if use_sklearn:
                gmm = GaussianMixture(n_components=n_components, random_state=42)
            else:
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
    plt.plot(range(1, max_clusters + 1), bic_scores, label='BIC')
    plt.plot(range(1, max_clusters + 1), aic_scores, label='AIC')
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

    print("Data shape:", X.shape)

    # 4.2 Determine the Optimal Number of Clusters for 512 dimensions
    print("\nTesting custom GMM class:")
    try:
        gmm = GMM(n_components=2)
        gmm.fit(X)
        print("Custom GMM class works on 512-dimensional data.")
    except Exception as e:
        print(f"Custom GMM class failed: {e}")

    print("\nTesting sklearn GMM class:")
    try:
        gmm_sklearn = GaussianMixture(n_components=2, random_state=42)
        gmm_sklearn.fit(X)
        print("Sklearn GMM class works on 512-dimensional data.")
    except Exception as e:
        print(f"Sklearn GMM class failed: {e}")

    # Use the working GMM class (not sklearn in this case) to find optimal clusters
    print("\nFinding optimal number of clusters using BIC and AIC:")
    kgmm1_bic, kgmm1_aic = find_optimal_clusters(X, max_clusters=10, use_sklearn=False)
    print(f"Optimal number of clusters (BIC): {kgmm1_bic}")
    print(f"Optimal number of clusters (AIC): {kgmm1_aic}")

    # Perform GMM on the dataset using kgmm1_bic
    print(f"\nPerforming GMM with {kgmm1_bic} clusters:")
    gmm_final = GMM(n_components=kgmm1_bic)

    # 6.3 part
    # gmm_final = GMM(n_components=4)

    gmm_final.fit(X)

    labels = gmm_final.getMembership(X).argmax(axis=1)


    # Plot using first two dimensions
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
    plt.colorbar(scatter)
    plt.title(f'GMM Clustering (K={kgmm1_bic}) on Dataset\nFirst Two Dimensions')
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.grid(True)
    plt.show()

    # Actually we cannot draw scatter plot for this so using t-SNE for visualization of high-dimensional data
    print("Applying t-SNE for visualization...")
    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X)

    # Plotting the results using t-SNE representation
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
    plt.colorbar(scatter)
    plt.title(f'GMM Clustering (K={kgmm1_bic}) on Dataset\nVisualized with t-SNE')
    plt.xlabel('t-SNE dimension 1')
    plt.ylabel('t-SNE dimension 2')
    plt.grid(True)
    plt.show()