import pandas as pd
import numpy as np
from collections import Counter
from tqdm import tqdm
import time

# Load and preprocess data
df = pd.read_csv('spotify.csv')
df = df.sample(random_state=36, frac=1).reset_index(drop=True)  # Shuffle data instead of sampling
df = df.dropna(subset=['artists', 'album_name', 'track_name'])
df = df.drop(columns=['Unnamed: 0'])
df = df.drop_duplicates(subset=['track_id']).reset_index(drop=True)

for column in ['artists', 'album_name', 'track_name', 'track_genre']:
    df[column] = df[column].astype('category').cat.codes

df = df.drop(columns=['track_id','duration_ms','explicit','key','mode','track_name'])

train_size = 0.8
test_size = 0.1
validation_size = 0.1

num_samples = len(df)
train_s = int(train_size * num_samples)
test_s = int(test_size * num_samples)
validation_s = int(validation_size * num_samples)

train_df = df[:train_s]
test_df = df[train_s:train_s + test_s]
validation_df = df[train_s + test_s:]


# Scaling function
def min_max_scaling(data):
    min_val = data.min(axis=0)
    max_val = data.max(axis=0)
    return (data - min_val) / (max_val - min_val)

# Normalizing the features
train_features = train_df.drop(columns=['track_genre']).values
validation_features = validation_df.drop(columns=['track_genre']).values
test_features = test_df.drop(columns=['track_genre']).values

X_train = min_max_scaling(train_features)
X_validation = min_max_scaling(validation_features)
X_test = min_max_scaling(test_features)

y_train = train_df['track_genre'].values
y_validation = validation_df['track_genre'].values
y_test = test_df['track_genre'].values

print("Training data shape:", train_df.shape)
print("Testing data shape:", test_df.shape)
print("Validation data shape:", validation_df.shape)

class KNN:
    def __init__(self, k=31, distance_metric='euclidean'):
        self.k = k
        self.distance_metric = distance_metric

        # Distance functions mapping
        self.distance_functions = {
            'euclidean': self.euclidean_distance,
            'manhattan': self.manhattan_distance
        }

        if self.distance_metric not in self.distance_functions:
            raise ValueError("Unsupported distance metric")

    def get_distance(self, x1, x2):
        distance_function = self.distance_functions[self.distance_metric]
        return distance_function(x1, x2)

    @staticmethod
    def euclidean_distance(x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2, axis=1))

    @staticmethod
    def manhattan_distance(x1, x2):
        return np.sum(np.abs(x1 - x2), axis=1)

    def get_neighbours(self, train_features, test_features):
        num_test_samples = test_features.shape[0]
        num_train_samples = train_features.shape[0]
        distances = np.zeros((num_test_samples, num_train_samples))
        
        for i in tqdm(range(num_test_samples), desc="Calculating distances", ncols=100):
            test_sample = test_features[i]
            distances[i] = self.get_distance(train_features, test_sample)
        
        nearest_neighbors = np.argsort(distances, axis=1)[:, :self.k]
        
        return nearest_neighbors


    def get_response(self, neighbors, train_labels):
        num_test_samples = neighbors.shape[0]
        most_common_labels = np.empty(num_test_samples, dtype=int)
        
        for i in range(num_test_samples):
            nearest_labels = train_labels[neighbors[i]]
            label_counts = np.bincount(nearest_labels)
            most_common_labels[i] = np.argmax(label_counts)
        return most_common_labels


    def predict(self, test_set):
        test_features = test_set.values
        neighbors = self.get_neighbours(X_train, test_features)
        predictions = self.get_response(neighbors, y_train)
        return predictions

knn = KNN(k=30, distance_metric='manhattan')

# Measuring time taken for prediction
start_time = time.time()
val_predictions = knn.predict(pd.DataFrame(X_validation))
end_time = time.time()

print(f"Time taken for prediction: {end_time - start_time:.2f} seconds")

# Define metrics functions
def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred) * 100

def precision_score(y_true, y_pred, average='macro'):
    labels = np.unique(y_true)
    precision_scores = []
    for label in labels:
        true_positive = np.sum((y_true == label) & (y_pred == label))
        false_positive = np.sum((y_true != label) & (y_pred == label))
        precision_scores.append(true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0)
    return np.mean(precision_scores)

def recall_score(y_true, y_pred, average='macro'):
    labels = np.unique(y_true)
    recall_scores = []
    for label in labels:
        true_positive = np.sum((y_true == label) & (y_pred == label))
        false_negative = np.sum((y_true == label) & (y_pred != label))
        recall_scores.append(true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0)
    return np.mean(recall_scores)

# def f1_score(y_true, y_pred):
#     precision = precision_score(y_true, y_pred)
#     recall = recall_score(y_true, y_pred)
#     return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

def macro_f1_score(y_true, y_pred):
    labels = np.unique(y_true)
    
    def calculate_f1_for_label(label):
        y_true_label = (y_true == label).astype(int)
        y_pred_label = (y_pred == label).astype(int)
        
        true_positive = np.sum((y_true_label == 1) & (y_pred_label == 1))
        false_positive = np.sum((y_true_label == 0) & (y_pred_label == 1))
        false_negative = np.sum((y_true_label == 1) & (y_pred_label == 0))
        
        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
        
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    f1_scores = np.array([calculate_f1_for_label(label) for label in labels])
    
    return np.mean(f1_scores)


def micro_f1_score(y_true, y_pred):
    labels = np.unique(y_true)
    
    true_positive = np.sum((y_true[:, None] == labels) & (y_pred[:, None] == labels), axis=0)
    false_positive = np.sum((y_true[:, None] != labels) & (y_pred[:, None] == labels), axis=0)
    false_negative = np.sum((y_true[:, None] == labels) & (y_pred[:, None] != labels), axis=0)
    
    total_true_positive = np.sum(true_positive)
    total_false_positive = np.sum(false_positive)
    total_false_negative = np.sum(false_negative)
    
    precision = total_true_positive / (total_true_positive + total_false_positive) if (total_true_positive + total_false_positive) > 0 else 0
    recall = total_true_positive / (total_true_positive + total_false_negative) if (total_true_positive + total_false_negative) > 0 else 0
    
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0


# Calculate and print metrics
accuracy = accuracy_score(y_validation, val_predictions)
precision = precision_score(y_validation, val_predictions)
recall = recall_score(y_validation, val_predictions)
# f1 = f1_score(y_validation, val_predictions)
macro_f1 = macro_f1_score(y_validation, val_predictions)
micro_f1 = micro_f1_score(y_validation, val_predictions)

print(f'Accuracy: {accuracy:.2f}%')
print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')
# print(f'F1 Score: {f1:.2f}')
print(f'Macro F1 Score: {macro_f1:.2f}')
print(f'Micro F1 Score: {micro_f1:.2f}')
