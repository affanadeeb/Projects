
# Assignment 1 Report

## 2.2 Exploratory Data Analysis

### 2.2.1 Task 1

After loading the dataset with the following code:

```python
df = pd.read_csv('spotify.csv')
```

and analyzing it using:

```python
df.head()
df.info()
```

we observe that the dataset has **114,000 rows** and **21 columns**.

#### Feature Distributions

I have plotted box plots, violin plots, histograms and regression plots for the various features(plots are in figures folder). Out of 21 different features 6 are of object dtype and other 15 are numerical data which i have shown in plots. Below is the distribution of each feature:

- **Acousticness:**  
  The distribution is U-shaped, indicating that many songs are either very high or very low in acousticness, with fewer songs falling in the middle range.

- **Valence:**  
  The distribution is relatively uniform, but there are slight peaks at both very low and very high valence levels.

- **Loudness:**  
  This feature has a left-skewed distribution, where most songs are clustered around higher loudness levels, with a smaller number of quieter songs extending the tail.

- **Instrumentalness:**  
  The distribution is extremely right-skewed, with most songs having very low instrumentalness, while a small number of songs are highly instrumental.

- **Liveness:**  
  This feature shows a right-skewed distribution, with most songs having low to moderate liveness, and a smaller number extending into higher liveness values.

- **Mode:**  
  The distribution is highly imbalanced, likely favoring the major mode over the minor, with one being far more common.

- **Popularity:**  
  The distribution is highly right-skewed, indicating that most songs have low popularity, while there's a small number of songs that are significantly more popular.

- **Energy:**  
  The distribution is relatively even, but we see a slight trend towards higher energy levels in most songs.

- **Duration_ms:**  
  This feature also shows a right-skewed distribution. Most songs have shorter durations, with fewer songs extending to longer lengths.

- **Speechiness:**  
  The distribution is extremely right-skewed, showing that most songs have very low speechiness, with a small number of songs featuring higher speechiness.

- **Danceability:**  
  The distribution is approximately normal but slightly left-skewed, meaning most songs have moderate danceability, with a slight tilt towards lower scores.

- **Key:**  
  The distribution is discrete and uneven, with some keys appearing much more frequently than others.

#### Correlation with Target Variable
From the correlation heatmap, we can visualize that:
- There is a comparitively high correlation between acousticness and genre. 
- There is a high positive correlation between energy and loudness.
- There is a high negative correlation between acousticness and energy.
### Hierarchy Based on Observations:

1. **Instrumentalness**
2. **Acousticness**
3. **Energy**
4. **Danceability**
5. **Speechiness**
6. **Tempo**
7. **Key, Mode, Time Signature**
8. **Duration_ms, Popularity**

This hierarchy reflects the impact of various features on genre classification. Features with greater variance in median values across genres are considered more influential. Conversely, features with numerous outliers are less useful, as they can distort the data. Additionally, features with similar median values across genres are deemed less impactful. This approach ensures we prioritize features that provide meaningful differentiation between genres while accounting for potential data distortions.

### 2.3.1 Task 2
I have created a KNN class with the given specifications.
### 2.4.1 Task 3
### 1).BEST {k, Distance Metric}
The optimal pair for {k, distance metric} that yields the highest validation accuracy for my code is (31, 'manhattan') with an accuracy of 34.82%.
## 2).Top 10 k Values with Highest Accuracy
1. **k = 30**: Accuracy: 34.82%
2. **k = 31**: Accuracy: 34.82%
3. **k = 32**: Accuracy: 34.81%
4. **k = 16**: Accuracy: 34.80%
5. **k = 23**: Accuracy: 34.80%
6. **k = 21**: Accuracy: 34.77%
7. **k = 14**: Accuracy: 34.72%
8. **k = 20**: Accuracy: 34.72%
9. **k = 13**: Accuracy: 34.70%
10. **k = 29**: Accuracy: 34.70%
## 3).Plot k vs accuracy
It is uploaded in figures folder
## 4,5) . 4 and Bonus
After testing various combinations and seeing the correlation heatmap, the optimal accuracy was achieved by dropping the columns **explicit**, **mode**, **track_id**, **key**, and **time_signature**.

### 2.5 Optimization
In the `KNN` class implementation, we've utilized vectorization to enhance performance by leveraging NumPy's efficient array operations. Here’s a simplified overview of how vectorization is applied:

1. **Distance Calculation**:
   - **Euclidean Distance**:
     ```python
     @staticmethod
     def euclidean_distance(x1, x2):
         return np.sqrt(np.sum((x1 - x2) ** 2, axis=1))
     ```
     Instead of looping through each element, we perform the distance calculation `(x1 - x2) ** 2` and `np.sum(..., axis=1)` on entire arrays at once. This approach takes full advantage of NumPy’s optimized operations to handle squared differences and their sum efficiently.

   - **Manhattan Distance**:
     ```python
     @staticmethod
     def manhattan_distance(x1, x2):
         return np.sum(np.abs(x1 - x2), axis=1)
     ```
     For the Manhattan distance, we use `np.abs(x1 - x2)` to compute absolute differences across arrays, and `np.sum(..., axis=1)` to aggregate these differences, avoiding explicit loops.

2. **Distance Matrix Calculation**:
   ```python
   distances[i] = self.get_distance(train_features, test_sample)
   ```
   When calculating distances, `self.get_distance(train_features, test_sample)` is applied to all test samples. This method leverages vectorized operations to compute distances efficiently between the training features and each test sample.

3. **Neighbor Indices**:
   ```python
   nearest_neighbors = np.argsort(distances, axis=1)[:, :self.k]
   ```
   After computing the distance matrix, we use `np.argsort` to get indices of the nearest neighbors for each test sample in a vectorized manner. This allows us to sort distances and retrieve the nearest neighbors efficiently without explicit loops.

4. **Label Aggregation**:
   ```python
   label_counts = np.bincount(nearest_labels)
   most_common_labels[i] = np.argmax(label_counts)
   ```
   In determining the most common labels among neighbors, `np.bincount` efficiently counts occurrences of each label. We then use `np.argmax` to find the most frequent label, all done through vectorized operations.

By applying these vectorized techniques, the `KNN` class avoids unnecessary loops and leverages NumPy's efficient array operations, resulting in faster and more efficient computations for distance calculations and label aggregations.

## 3 Linear Regression

### 3.1.1

## Metrics (Degree: 1)
- **Training MSE:** 0.3449
- **Testing MSE:** 0.2818
- **Training Standard Deviation:** 0.9208
- **Testing Standard Deviation:** 0.9050
- **Training Variance:** 0.8480
- **Testing Variance:** 0.8190

### 3.1.2


## Polynomial Regression Metrics

| Degree | Training MSE | Testing MSE | Training Standard Deviation | Testing Standard Deviation | Training Variance | Testing Variance |
|--------|--------------|-------------|-----------------------------|----------------------------|-------------------|------------------|
| **1**  | 0.3449       | 0.2818      | 0.9208                      | 0.9050                     | 0.8480            | 0.8190           |
| **2**  | 0.2337       | 0.2065      | 0.9793                      | 0.9805                     | 0.9591            | 0.9614           |
| **3**  | 0.0760       | 0.0613      | 1.0568                      | 0.9893                     | 1.1168            | 0.9787           |
| **4**  | 0.0760       | 0.0615      | 1.0568                      | 0.9895                     | 1.1168            | 0.9791           |
| **5**  | 0.0248       | 0.0201      | 1.0808                      | 1.0211                     | 1.1681            | 1.0426           |

**Best Degree:** 5  
**Best Testing MSE:** 0.0201

### 3.2 Regularization


## MSE for Different Polynomial Degrees and Regularization Techniques

| Degree | Regularization       | MSE (Train) | MSE (Val) |
|--------|----------------------|-------------|-----------|
| **1**  | No Regularization     | 0.2137      | 0.2273    |
| **1**  | L1 Regularization     | 0.2137      | 0.2275    |
| **1**  | L2 Regularization     | 0.2137      | 0.2273    |
| **5**  | No Regularization     | 0.0123      | 0.0161    |
| **5**  | L1 Regularization     | 0.0122      | 0.0158    |
| **5**  | L2 Regularization     | 0.0123      | 0.0160    |
| **10** | No Regularization     | 0.0128      | 0.0182    |
| **10** | L1 Regularization     | 0.0128      | 0.0181    |
| **10** | L2 Regularization     | 0.0128      | 0.0182    |
| **15** | No Regularization     | 0.0114      | 0.0151    |
| **15** | L1 Regularization     | 0.0115      | 0.0151    |
| **15** | L2 Regularization     | 0.0114      | 0.0151    |
| **20** | No Regularization     | 0.0113      | 0.0165    |
| **20** | L1 Regularization     | 0.0114      | 0.0161    |
| **20** | L2 Regularization     | 0.0113      | 0.0164    |


**Obseravtions:** Bboth **L1** and **L2** regularizations effectively reduce the Mean Squared Error (MSE) for larger values of \( K \). However, for smaller values of \( K \), the MSE values remain nearly identical across all three cases.





---

