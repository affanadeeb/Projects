import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df1 = pd.read_csv('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\k_means.csv')

# print(df.head()) #gives first 5 rows data (i can also mention head(10) if i want 10 rows) 
# print(df.info()) # gives content in the data i.e what each coloumn is representing
# print(df.describe()) #This gives mean,count and other mathematical parameters for the eacch coloumn data

df = pd.read_feather('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\word-embeddings.feather')

print(df.columns) 
# print(df.head())  
print(df.shape)

# Extracting embeddings
X = np.array(df['vit'].tolist())

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

# Elbow Method: Varying k and computing WCSS for each k
wcss = []
K = range(1, 20)  
for k in K:
    kmeans = KMeans(k=k)
    kmeans.fit(X)
    # print(kmeans.getCost(X))
    wcss_i = kmeans.getCost(X)
    print(wcss_i)
    wcss.append(wcss_i)

# Plotting the Elbow curve
plt.figure(figsize=(8, 6))
plt.plot(K, wcss)
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters (k)')
plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
plt.grid(True)
plt.show()

# After inspecting the plot, 
kkmeans1 = 2  # elbow point is at k = 2

# Perform K-means clustering with the optimal number of clusters
kmeans_optimal = KMeans(k=kkmeans1)
kmeans_optimal.fit(X)

# Predict the clusters
labels_optimal = kmeans_optimal.predict(X)

# Add the predicted cluster labels to the dataframe
df['Cluster'] = labels_optimal

# I tried to plot the scatter plot as below but i am not getting it because of 512 dimensions.

# plt.figure(figsize=(10, 8))
# plt.scatter(X[:, 0], X[:, 1], c=df['Cluster'], cmap='Set1', s=100, alpha=0.7)

# # Mark the centroids on the plot
# centroids = kmeans_optimal.centroids
# plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=200, marker='X', label='Centroids')

# plt.title('K-Means Clustering with k=3')
# plt.xlabel('Feature 1')
# plt.ylabel('Feature 2')
# plt.legend()
# plt.grid(True)
# plt.show()

print(df.head())




# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
# Testing for the given example csv file in Moodle Assignment-2 thread
# dropping non-numeric columns if any
X = df1.select_dtypes(include=[np.number]).values

kmeans = KMeans(k=3, max_iters=100)

# kmeans = KMeans(k=4, max_iters=100) # 6.1 task

# Fitting the model
kmeans.fit(X)
labels = kmeans.predict(X)

df1['Cluster'] = labels

sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette='viridis')
plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], s=300, c='red', label='Centroids')
plt.legend()
plt.title("K-Means Clustering Results")
plt.show()

#printing the cost (WCSS)
cost = kmeans.getCost(X)
print(f"Within-Cluster Sum of Squares for testing dataset given in A2-thread (WCSS):{cost}")