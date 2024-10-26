import pandas as pd
import numpy as np
from collections import Counter
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

from pca import PCA  
df = pd.read_csv('C:\\Users\\Affan\\Documents\\SMAI\\smai-m24-assignments-affanshaik2005\\data\\external\\spotify.csv')

df = df.sample(random_state=36, frac=1).reset_index(drop=True)
# df = df.dropna(subset=['artists', 'album_name', 'track_name'])
df = df.drop(columns=['Unnamed: 0'])
df = df.drop_duplicates(subset=['track_id']).reset_index(drop=True)

for column in ['artists', 'album_name', 'track_name', 'track_genre']:
    df[column] = df[column].astype('category').cat.codes

df = df.drop(columns=['track_id', 'duration_ms', 'explicit', 'key', 'mode', 'track_name'])

# Split the dataset
train_size = 0.8
validation_size = 0.2

num_samples = len(df)
train_s = int(train_size * num_samples)

train_df = df[:train_s]
validation_df = df[train_s:]

# Scaling function
def min_max_scaling(data):
    min_val = data.min(axis=0)
    max_val = data.max(axis=0)
    return (data - min_val) / (max_val - min_val)

# Normalizing the features
train_features = train_df.drop(columns=['track_genre']).values
validation_features = validation_df.drop(columns=['track_genre']).values

X_train = min_max_scaling(train_features)
X_validation = min_max_scaling(validation_features)

y_train = train_df['track_genre'].values
y_validation = validation_df['track_genre'].values

# Applying PCA
pca_full = PCA(n_components=X_train.shape[1])  # Initialize with max components
pca_full.fit(X_train)

# Generate scree plot
explained_variance = np.var(pca_full.transform(X_train), axis=0)
explained_variance_ratio = explained_variance / np.sum(explained_variance)

plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, 'bo-')
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Proportion of Variance Explained')
plt.show()

# dimensions based on scree plot observation
n_dimensions = 3 

print(f"Number of dimensions chosen: {n_dimensions}")

# Apply PCA with 3 dimensions
pca_reduced = PCA(n_components=n_dimensions)
pca_reduced.fit(X_train)
X_train_pca = pca_reduced.transform(X_train)
X_validation_pca = pca_reduced.transform(X_validation)

# Calculating cumulative explained variance ratio
cumulative_variance_ratio = np.cumsum(explained_variance_ratio[:n_dimensions])
print(f"Cumulative explained variance ratio with {n_dimensions} dimensions: {cumulative_variance_ratio[-1]:.4f}")

class KNN:
    def __init__(self, k=31):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def manhattan_distance(self, x1, x2):
        return np.sum(np.abs(x1 - x2), axis=1)

    def get_neighbors(self, test_sample):
        distances = self.manhattan_distance(self.X_train, test_sample)
        return np.argsort(distances)[:self.k]

    def predict(self, X_test):
        predictions = []
        for sample in tqdm(X_test, desc="Predicting"):
            neighbors = self.get_neighbors(sample)
            votes = self.y_train[neighbors]
            prediction = Counter(votes).most_common(1)[0][0]
            predictions.append(prediction)
        return np.array(predictions)

def calculate_metrics(y_true, y_pred):
    accuracy = np.mean(y_true == y_pred)
    
    precision_list = []
    recall_list = []
    f1_list = []
    
    unique_labels = np.unique(y_true)
    
    for label in unique_labels:
        true_positives = np.sum((y_true == label) & (y_pred == label))
        false_positives = np.sum((y_true != label) & (y_pred == label))
        false_negatives = np.sum((y_true == label) & (y_pred != label))
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        precision_list.append(precision)
        recall_list.append(recall)
        f1_list.append(f1)
    
    return {
        'accuracy': accuracy,
        'precision': np.mean(precision_list),
        'recall': np.mean(recall_list),
        'f1_score': np.mean(f1_list)
    }

# KNN on complete dataset
knn_complete = KNN(k=31)
knn_complete.fit(X_train, y_train)

start_time = time.time()
y_pred_complete = knn_complete.predict(X_validation)
end_time = time.time()
inference_time_complete = end_time - start_time

metrics_complete = calculate_metrics(y_validation, y_pred_complete)

# KNN on PCA-reduced dataset
knn_pca = KNN(k=31)
knn_pca.fit(X_train_pca, y_train)

start_time = time.time()
y_pred_pca = knn_pca.predict(X_validation_pca)
end_time = time.time()
inference_time_pca = end_time - start_time

metrics_pca = calculate_metrics(y_validation, y_pred_pca)

# Print results
print("\nComplete Dataset Metrics:")
for metric, value in metrics_complete.items():
    print(f"{metric.capitalize()}: {value:.4f}")
print(f"Inference Time: {inference_time_complete:.2f} seconds")

print("\nPCA-Reduced Dataset Metrics:")
for metric, value in metrics_pca.items():
    print(f"{metric.capitalize()}: {value:.4f}")
print(f"Inference Time: {inference_time_pca:.2f} seconds")

# Plot inference times
plt.figure(figsize=(10, 6))
plt.bar(['Complete Dataset', 'PCA-Reduced Dataset'], [inference_time_complete, inference_time_pca])
plt.title('KNN Inference Time Comparison')
plt.ylabel('Time (seconds)')
plt.show()

# Comparison analysis
print("\nComparison Analysis:")
for metric in metrics_complete.keys():
    diff = metrics_pca[metric] - metrics_complete[metric]
    print(f"{metric.capitalize()} difference (PCA - Complete): {diff:.4f}")

print(f"\nInference Time Reduction: {inference_time_complete - inference_time_pca:.2f} seconds")
print(f"Inference Time Improvement: {(1 - inference_time_pca / inference_time_complete) * 100:.2f}%")