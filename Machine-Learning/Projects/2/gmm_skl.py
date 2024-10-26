import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

df = pd.read_feather('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\word-embeddings.feather')

print(df.shape)
print(df.columns)

X = np.array(df['vit'].tolist())

# Range of clusters
n_components_range = range(1, 11)

bic = []
aic = []

# Fitting GMM for each number of components and storing BIC/AIC
for n in n_components_range:
    gmm = GaussianMixture(n_components=n, max_iter=100, tol=1e-4, reg_covar=1e-6)
    gmm.fit(X)
    bic.append(gmm.bic(X))
    aic.append(gmm.aic(X))

# Plotting BIC and AIC to visualize the optimal number of clusters
plt.figure(figsize=(10, 5))
plt.plot(n_components_range, bic, label='BIC')
plt.plot(n_components_range, aic, label='AIC')
plt.xlabel('Number of components (clusters)')
plt.ylabel('Criterion')
plt.title('BIC and AIC for different number of clusters')
plt.legend()
plt.show()

# Determining the optimal number of clusters 
kgmm1_bic = n_components_range[np.argmin(bic)]
kgmm1_aic = n_components_range[np.argmin(aic)]

print(f"Optimal number of clusters based on BIC: {kgmm1_bic}")
print(f"Optimal number of clusters based on AIC: {kgmm1_aic}")

# Choosing kgmm1 based on BIC (we can also change it to AIC)
kgmm1 = kgmm1_bic

# kgmm1 = 4 # 6.3 task

# Fitting GMM with the optimal number of clusters
gmm_optimal = GaussianMixture(n_components=kgmm1, max_iter=100, tol=1e-4, reg_covar=1e-6)
gmm_optimal.fit(X)

# GMM parameters for kgmm1
optimal_means = gmm_optimal.means_
optimal_covariances = gmm_optimal.covariances_
optimal_weights = gmm_optimal.weights_
optimal_memberships = gmm_optimal.predict_proba(X)
optimal_log_likelihood = gmm_optimal.score(X) * X.shape[0]  # Total log-likelihood

#results
print(f"GMM Results for kgmm1 = {kgmm1}:")
print("Means:", optimal_means)
print("Covariances:", optimal_covariances)
print("Weights:", optimal_weights)
print("Memberships (first 5):", optimal_memberships[:5])  
print("Log-likelihood:", optimal_log_likelihood)


# Scatter plot to visualize clusters
cluster_labels = gmm_optimal.predict(X)

# Get unique colors for clusters using a colormap
colors = plt.cm.get_cmap('tab10', kgmm1)

plt.figure(figsize=(10, 8))
for i in range(kgmm1):
    plt.scatter(X[cluster_labels == i, 0], X[cluster_labels == i, 1], 
                label=f'Cluster {i+1}', color=colors(i))

# Plot centroids with the same color as respective clusters
for i in range(kgmm1):
    plt.scatter(optimal_means[i, 0], optimal_means[i, 1], 
                s=300, c=[colors(i)], marker='X', label=f'Centroid {i+1}')

plt.title(f'GMM Clustering with {kgmm1} Components')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()
