import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy as hc
from scipy.spatial.distance import pdist
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import fcluster

df = pd.read_feather('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\word-embeddings.feather')
X = np.stack(df['vit'].values)

# Function to perform hierarchical clustering and plot dendrogram
def plot_dendrogram(X, linkage_method, distance_metric='euclidean'):
    # Computing the distance matrix
    dist_matrix = pdist(X, metric=distance_metric)
    
    # hierarchical clustering and computing linkage matrix
    Z = hc.linkage(dist_matrix, method=linkage_method)
    
    # Plot the dendrogram
    plt.figure(figsize=(10, 7))
    hc.dendrogram(Z)
    plt.title(f'Hierarchical Clustering Dendrogram\nLinkage: {linkage_method}, Distance: {distance_metric}')
    plt.xlabel('Sample Index')
    plt.ylabel('Distance')
    plt.show()
    
    return Z

# Experimenting with different linkage methods and distance metrics
linkage_methods = ['single', 'complete', 'average', 'ward']
distance_metrics = ['euclidean', 'cityblock', 'cosine', 'correlation']

for method in linkage_methods:
    for metric in distance_metrics:
        # Ward method only works with Euclidean distance
        if method == 'ward' and metric != 'euclidean':
            continue
        
        print(f"\nExperimenting with Linkage: {method}, Distance: {metric}")
        Z = plot_dendrogram(X, method, metric)
        print("Linkage Matrix (first 5 rows):")
        print(Z[:5])

# Function to perform clustering and compare with K-means and GMM
def compare_clustering(X, Z, k, linkage_method):
    # Hierarchical clustering
    hc_labels = fcluster(Z, k, criterion='maxclust')
    
    # K-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans_labels = kmeans.fit_predict(X)
    
    # GMM clustering
    gmm = GaussianMixture(n_components=k, random_state=42)
    gmm_labels = gmm.fit_predict(X)
    
    # Compare cluster assignments
    print(f"Comparison for k={k}:")
    print("Hierarchical Clustering:", hc_labels[:10])
    print("K-means Clustering:     ", kmeans_labels[:10])
    print("GMM Clustering:         ", gmm_labels[:10])
    print("\n")
    
    return hc_labels, kmeans_labels, gmm_labels

# Plot clusters in 2D space using PCA for comparison
def plot_cluster_comparison(X, hc_labels, kmeans_labels, gmm_labels, k_hc, k_kmeans, k_gmm, title):
    # Reducing dimensionality for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    
    plt.figure(figsize=(15, 5))

    # Hierarchical Clustering results
    plt.subplot(1, 3, 1)  
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=hc_labels, cmap='viridis', s=50)
    plt.title(f'Hierarchical Clustering (k={k_hc})\n{title}')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    
    # K-means Clustering results
    plt.subplot(1, 3, 2)  # 1 row, 3 columns, 2nd subplot
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans_labels, cmap='viridis', s=50)
    plt.title(f'K-means Clustering (k={k_kmeans})')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    
    # GMM Clustering results
    plt.subplot(1, 3, 3)  # 1 row, 3 columns, 3rd subplot
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=gmm_labels, cmap='viridis', s=50)
    plt.title(f'GMM Clustering (k={k_gmm})')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')

    # Adjust layout to avoid overlap and improve spacing
    plt.tight_layout()
    plt.show()

kbest1, kbest2 = 2, 4

# Choosing the best linkage method: ward provides clear, well-separated, and stable clusters based 
# on visual inspection, clustering metrics, and comparison with other clustering methods.
best_linkage_method = 'ward'

# Perform hierarchical clustering with the best linkage method
Z_best = plot_dendrogram(X, best_linkage_method)

# Compare clustering results and visualize
hc_labels_3, kmeans_labels_3, gmm_labels_3 = compare_clustering(X, Z_best, kbest1, best_linkage_method)
hc_labels_4, kmeans_labels_4, gmm_labels_4 = compare_clustering(X, Z_best, kbest2, best_linkage_method)

# Plot comparison for kbest1 clusters (K-means best)
plot_cluster_comparison(X, hc_labels_3, kmeans_labels_3, gmm_labels_3, kbest1, kbest1, kbest1, f'k={kbest1}')

# Plot comparison for kbest2 clusters (GMM best)
plot_cluster_comparison(X, hc_labels_4, kmeans_labels_4, gmm_labels_4, kbest2, kbest2, kbest2, f'k={kbest2}')
