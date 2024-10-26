import pandas as pd
import numpy as np
import math
import operator
from collections import Counter

df = pd.read_csv('spotify.csv')
df = df.dropna(subset=['artists', 'album_name', 'track_name'])
df = df.drop(columns=['Unnamed: 0'])
df = df.drop_duplicates(subset=['track_id'], keep='first')

sample_size = 1000 
df = df.sample(n=sample_size, random_state=1)

for column in ['artists', 'album_name', 'track_name', 'track_genre']:
    df[column] = df[column].astype('category').cat.codes

df = df.drop(columns=['track_id'])
df['explicit'] = df['explicit'].astype(int)

train = 0.8
test = 0.1
validation = 0.1

train_s = int(train * len(df))
test_s = int(test * len(df))
validation_s = int(validation * len(df))

train_df = df[:train_s]
test_df = df[train_s:train_s + test_s]
validation_df = df[train_s + test_s:]

train_df.to_csv("train.csv")
test_df.to_csv("test.csv")
validation_df.to_csv("validation.csv")

print("Training data shape:", train_df.shape)
print("Testing data shape:", test_df.shape)
print("Validation data shape:", validation_df.shape)

class KNN:
    def __init__(self, k=30, distance_metric='euclidean'):
        self.k = k
        self.distance_metric = distance_metric
        self.distance_functions = {
            'euclidean': self.euclidean_distance,
            'manhattan': self.manhattan_distance
        }

        if self.distance_metric not in self.distance_functions:
            raise ValueError("Unsupported distance metric")
        
    def get_distance(self, x1, x2):
        distance_function = self.distance_functions[self.distance_metric]
        return distance_function(x1, x2)

    def set_params(self, k=None, distance_metric=None):
        if k is not None:
            self.k = k
        if distance_metric is not None:
            self.distance_metric = distance_metric

    def euclidean_distance(self, data_x, data_y, length):
        dist = 0
        for x in range(length):
            dist += pow((data_x[x] - data_y[x]), 2)
        return math.sqrt(dist)

    def manhattan_distance(self, data_x, data_y, length):
        dist = 0
        for x in range(length):
            dist += abs(data_x[x] - data_y[x])
        return dist

    def get_neighbours(self, trainingSet, testSet, k):
        dist = []
        length = len(testSet) - 1  
        test_values = testSet.values[:-1]  

        for index in range(len(trainingSet)):
            train_values = trainingSet.iloc[index].values[:-1]  
            dist_dum = self.get_distance(test_values, train_values, length)
            dist.append((trainingSet.iloc[index], dist_dum))

        dist.sort(key=operator.itemgetter(1))
        neighbours = [dist[i][0] for i in range(k)]
        return neighbours

    def get_response(self, neighbours):
        classVotes = Counter(neighbour['track_genre'] for neighbour in neighbours)
        return classVotes.most_common(1)[0][0]

    def predict(self, test_set):
        predictions = []
        for index, test_instance in test_set.iterrows():
            neighbours = self.get_neighbours(train_df, test_instance, self.k)
            result = self.get_response(neighbours)
            predictions.append(result)
        return predictions


class Metrics:
    @staticmethod
    def get_accuracy(y_true, y_pred):
        correct = sum(a == p for a, p in zip(y_true, y_pred))
        return correct / len(y_true) * 100

    @staticmethod
    def precision(y_true, y_pred):
        true_positive_counts = np.zeros(len(set(y_true)))
        predicted_positive_counts = np.zeros(len(set(y_true)))

        for i, (true_label, predicted_label) in enumerate(zip(y_true, y_pred)):
            true_positive_counts[true_label] += true_label == predicted_label
            predicted_positive_counts[predicted_label] += 1

        precision_scores = [true_positive / predicted_positive if predicted_positive > 0 else 0.0 for true_positive, predicted_positive in zip(true_positive_counts, predicted_positive_counts)]

        return np.mean(precision_scores)

    @staticmethod
    def recall(y_true, y_pred):

        true_positive_counts = np.zeros(len(set(y_true)))
        actual_positive_counts = np.zeros(len(set(y_true)))

        for i, (true_label, predicted_label) in enumerate(zip(y_true, y_pred)):
            true_positive_counts[true_label] += true_label == predicted_label
            actual_positive_counts[true_label] += 1

        recall_scores = [true_positive / actual_positive if actual_positive > 0 else 0.0 for true_positive, actual_positive in zip(true_positive_counts, actual_positive_counts)]

        return np.mean(recall_scores)

    def f1_score(y_true, y_pred):
        precision = precision(y_true, y_pred)
        recall = recall(y_true, y_pred)

        return 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0

    def macro_f1_score(y_true, y_pred):
        unique_labels = set(y_true)
        f1_scores = []

        for class_label in unique_labels:
            true_positive = sum((a == p) and (p == class_label) for a, p in zip(y_true, y_pred))
            predicted_positive = sum(p == class_label for p in y_pred)
            actual_positive = sum(a == class_label for a in y_true)

            precision = true_positive / predicted_positive if predicted_positive > 0 else 0.0
            recall = true_positive / actual_positive if actual_positive > 0 else 0.0

            f1_scores.append(2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0)

        return np.mean(f1_scores)

    def micro_f1_score(y_true, y_pred):

        true_positive = sum((a == p) for a, p in zip(y_true, y_pred))
        predicted_positive = len(y_pred)
        actual_positive = len(y_true)

        precision = true_positive / predicted_positive if predicted_positive > 0 else 0.0
        recall = true_positive / actual_positive if actual_positive > 0 else 0.0

        return 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0


knn = KNN(k=11, distance_metric='euclidean')
val_predictions = knn.predict(validation_df)
val_labels = validation_df['track_genre'].values

# Calculating metrics
accuracy = Metrics.get_accuracy(val_labels, val_predictions)
precision = Metrics.precision(val_labels, val_predictions)
recall = Metrics.recall(val_labels, val_predictions)
f1 = Metrics.f1_score(val_labels, val_predictions)
macro_f1 = Metrics.macro_f1_score(val_labels, val_predictions)
micro_f1 = Metrics.micro_f1_score(val_labels, val_predictions)

print(f"Validation Accuracy: {accuracy:.2f}%")
print(f"Validation Precision: {precision:.2f}")
print(f"Validation Recall: {recall:.2f}")
print(f"Validation F1 Score: {f1:.2f}")
print(f"Validation Macro F1 Score: {macro_f1:.2f}")
print(f"Validation Micro F1 Score: {micro_f1:.2f}")