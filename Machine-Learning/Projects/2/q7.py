import sys
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from scipy.special import logsumexp  # Required for GMM

sys.path.append("C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\models")
from kmeans_class import KMeans
from gmm_class import GMM

# Load the data
df = pd.read_feather('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\word-embeddings.feather')
X = np.stack(df['vit'].values)
words = df['words'].values


def analyze_kmeans(X, k_values):
    results = {}
    for k in k_values:
        kmeans = KMeans(k=k)
        kmeans.fit(X)
        labels = kmeans.predict(X)
        silhouette = silhouette_score(X, labels)
        cost = kmeans.getCost(X)
        results[k] = {'labels': labels, 'silhouette': silhouette, 'cost': cost}
    return results

def analyze_gmm(X, k_values):
    results = {}
    for k in k_values:
        print(f"Running GMM for k={k}...")
        gmm = GMM(n_components=k)
        gmm.fit(X)  # Fit the custom GMM model

        # Get membership (i.e., predicted labels)
        labels = np.argmax(gmm.getMembership(X), axis=1)

        # For all k, compute log-likelihood
        log_likelihood = gmm.getLikelihood(X)
        results[k] = {'labels': labels, 'log_likelihood': log_likelihood}
    
    return results

# Printing a few samples from each cluster
# def print_cluster_samples(labels, words, n_samples=5):
#     unique_labels = np.unique(labels)
#     for label in unique_labels:
#         cluster_words = words[labels == label][:n_samples]
#         print(f"Cluster {label}: {', '.join(cluster_words)}")

# 7.1 K-Means analysis for different k values
kmeans_k_values = [3, 4, 2]  # K_kmeans1, K2, K_kmeans3
kmeans_results = analyze_kmeans(X, kmeans_k_values)

print("K-Means Results:")
for k, result in kmeans_results.items():
    print(f"k={k}:")
    print(f"  Silhouette Score: {result['silhouette']:.4f}")
    # print_cluster_samples(result['labels'], words)
    print()

# 7.2 GMM analysis for different k values
gmm_k_values = [1, 4, 3]  # K_gmm1, K2, K_gmm3
gmm_results = analyze_gmm(X, gmm_k_values)

print("GMM Results:")
for k, result in gmm_results.items():
    print(f"k={k}:")
    print(f"  Log-Likelihood: {result['log_likelihood']:.4f}")
    # print_cluster_samples(result['labels'], words)
    print()

# Determine the best k for K-Means and GMM
kkmeans = 2  # K-Means with k=2
kgmm = 4     # GMM with k=4

# Calculate Silhouette Score for GMM with k=4
gmm_silhouette = silhouette_score(X, gmm_results[kgmm]['labels'])

print(f"Best k for K-Means (kkmeans): {kkmeans}")
print(f"Best k for GMM (kgmm): {kgmm}")

# Comparison of best K-Means and GMM results
print("\nComparison of Best K-Means and GMM Results:")
print(f"K-Means (k={kkmeans}) - Silhouette Score: {kmeans_results[kkmeans]['silhouette']:.4f}")
# print_cluster_samples(kmeans_results[kkmeans]['labels'], words)

print(f"\nGMM (k={kgmm}) - Log-Likelihood: {gmm_results[kgmm]['log_likelihood']:.4f}")
print(f"GMM (k={kgmm}) - Silhouette Score: {gmm_silhouette:.4f}")
# print_cluster_samples(gmm_results[kgmm]['labels'], words)

# Determine which model has the better performance based on Silhouette Score
kmeans_score = kmeans_results[kkmeans]['silhouette']
gmm_score = gmm_silhouette

print("\nWhich model performs better based on Silhouette Score?")
if kmeans_score > gmm_score:
    print(f"K-Means with k={kkmeans} has a higher Silhouette Score ({kmeans_score:.4f}) compared to GMM with k={kgmm} ({gmm_score:.4f}).")
elif gmm_score > kmeans_score:
    print(f"GMM with k={kgmm} has a higher Silhouette Score ({gmm_score:.4f}) compared to K-Means with k={kkmeans} ({kmeans_score:.4f}).")
else:
    print(f"K-Means with k={kkmeans} and GMM with k={kgmm} have the same Silhouette Score ({kmeans_score:.4f}).")
