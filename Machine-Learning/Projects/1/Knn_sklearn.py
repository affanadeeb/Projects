from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd

# Load and preprocess data
df = pd.read_csv('spotify.csv')
df = df.sample(random_state=36, frac=1).reset_index(drop=True)
df = df.dropna(subset=['artists', 'album_name', 'track_name'])
df = df.drop(columns=['Unnamed: 0'])
df = df.drop_duplicates(subset=['track_id']).reset_index(drop=True)

for column in ['artists', 'album_name', 'track_name', 'track_genre']:
    df[column] = df[column].astype('category').cat.codes

df = df.drop(columns=['track_id', 'duration_ms', 'explicit', 'key', 'mode', 'track_name'])

# Splitting data
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

# Scaling
scaler = MinMaxScaler()
X_train = scaler.fit_transform(train_df.drop(columns=['track_genre']))
X_validation = scaler.transform(validation_df.drop(columns=['track_genre']))
X_test = scaler.transform(test_df.drop(columns=['track_genre']))

y_train = train_df['track_genre'].values
y_validation = validation_df['track_genre'].values
y_test = test_df['track_genre'].values

# KNN model
knn = KNeighborsClassifier(n_neighbors=4, metric='manhattan')
knn.fit(X_train, y_train)
val_predictions = knn.predict(X_validation)

# Metrics
accuracy = accuracy_score(y_validation, val_predictions)*100
precision = precision_score(y_validation, val_predictions, average='macro')
recall = recall_score(y_validation, val_predictions, average='macro')
f1 = f1_score(y_validation, val_predictions, average='macro')

print(f'Accuracy: {accuracy:.2f}%')
print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')
print(f'F1 Score: {f1:.2f}')
