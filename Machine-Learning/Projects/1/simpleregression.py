import numpy as np
import matplotlib.pyplot as plt
import pickle

data = np.genfromtxt('C:/Users/Affan/Desktop/python/linreg.csv', delimiter=',', skip_header=1)

np.random.shuffle(data)

# print(data.shape)
# print(data[:5])

train=0.8
test=0.1
validation=0.1

train_s=int(train*len(data))
test_s=int(test*len(data))
validation_s=int(validation*len(data))

train_data=data[:train_s]
test_data=data[train_s:train_s + test_s]
validation_data=data[train_s+test_s:]
print("Training data shape:", train_data.shape)
print("Testing data shape:", test_data.shape)
print("Validation data shape:", validation_data.shape)

x_train, y_train = train_data.T
x_test, y_test = test_data.T
x_val, y_val = validation_data.T


plt.figure(figsize=(10, 6))

plt.scatter(x_train, y_train, color='blue', label='Training Data', alpha=0.6)
plt.scatter(x_test, y_test, color='green', label='Testing Data', alpha=0.6)
plt.scatter(x_val, y_val, color='red', label='Validation Data', alpha=0.6)

plt.title('Visualization of Data Splits')
plt.xlabel('x (Independent Variable)')
plt.ylabel('y (Dependent Variable)')
plt.legend()
plt.grid(True)

plt.show()

# 3.3.1
# My method to find y=mx+c line
mean_x = np.mean(x_train)
mean_y = np.mean(y_train)

# Calculating the coefficients m (slope) and c (intercept) 
sum1 = 0
sum2 = 0
for i, j in zip(x_train, y_train):
    sum1 += (i - mean_x) * (j - mean_y)
    sum2 += (i - mean_x) ** 2

m = sum1 / sum2
c = mean_y - (m * mean_x)

# Predicted values for training, testing, and validation sets
y_train_pred = m * x_train + c
y_test_pred = m * x_test + c
y_val_pred = m * x_val + c

# # Calculating MSE, standard deviation, and variance for training data
# mse_train = np.mean((y_train - y_train_pred) ** 2)
# std_train = np.std(y_train - y_train_pred)
# variance_train = np.var(y_train - y_train_pred)

# # Calculating MSE, standard deviation, and variance for testing data
# mse_test = np.mean((y_test - y_test_pred) ** 2)
# std_test = np.std(y_test - y_test_pred)
# variance_test = np.var(y_test - y_test_pred)

# # Calculating MSE, standard deviation, and variance for validation data
# mse_val = np.mean((y_val - y_val_pred) ** 2)
# std_val = np.std(y_val - y_val_pred)
# variance_val = np.var(y_val - y_val_pred)



# Plotting
max_x = np.max(x_train)
min_x = np.min(x_train)
max_y = np.max(y_train)
min_y = np.min(y_train)
x_range_extension = 0.2 
y_range_extension = 0.5 
x_values = np.linspace(min_x - x_range_extension, max_x + x_range_extension, 100)
y_values = m * x_values + c

plt.figure(figsize=(12, 8))
plt.plot(x_values, y_values, color='red', label='Regression Line')
plt.scatter(x_train, y_train, color='blue', label='Training Data Points', alpha=0.7)
plt.scatter(x_test, y_test, color='green', label='Testing Data Points', alpha=0.7)
plt.scatter(x_val, y_val, color='orange', label='Validation Data Points', alpha=0.7)
plt.xlim(min_x - x_range_extension, max_x + x_range_extension)
plt.ylim(min_y - y_range_extension, max_y + y_range_extension)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression Plot')
plt.legend()
plt.grid(True)
plt.show()


# Gradient descent for experiment with different learning rates
X_train_b = np.c_[np.ones((x_train.shape[0], 1)), x_train.reshape(-1, 1)]
X_test_b = np.c_[np.ones((x_test.shape[0], 1)), x_test.reshape(-1, 1)]
X_val_b = np.c_[np.ones((x_val.shape[0], 1)), x_val.reshape(-1, 1)]

def gradient_descent(X, y, learning_rate, n_iterations):
    m = len(y)
    theta = np.zeros(X.shape[1])
    for iteration in range(n_iterations):
        gradients = 2/m * X.T @ (X @ theta - y)
        theta = theta - learning_rate * gradients
    return theta

#  mean squared error
def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Experiment with different learning rates
learning_rates = [0.001, 0.01, 0.1, 0.5]
n_iterations = 1000
best_learning_rate = None
best_mse = float('inf')
best_theta = None

for lr in learning_rates:
    theta = gradient_descent(X_train_b, y_train, lr, n_iterations)
    y_val_pred = X_val_b @ theta
    mse = mean_squared_error(y_val, y_val_pred)
    print(f"Learning Rate: {lr}, Validation MSE: {mse}")
    if mse < best_mse:
        best_mse = mse
        best_learning_rate = lr
        best_theta = theta

print(f"\nBest Learning Rate: {best_learning_rate}, Best Validation MSE: {best_mse}")

# Using the best theta to make predictions
y_train_pred = X_train_b @ best_theta
y_test_pred = X_test_b @ best_theta
y_val_pred = X_val_b @ best_theta

# Computing Variance
def variance(y):
    return np.mean((y - np.mean(y)) ** 2)

# metrics printing
def report_metrics(y_true, y_pred, name):
    print(f"\n{name} Metrics:")
    print(f"Mean Squared Error: {mean_squared_error(y_true, y_pred)}")
    print(f"Variance of {name}: {variance(y_pred)}")
    print(f"Standard Deviation of {name}: {np.std(y_pred)}")

report_metrics(y_train, y_train_pred, "Training")
report_metrics(y_test, y_test_pred, "Testing")
report_metrics(y_val, y_val_pred, "Validation")


y_train_pred = X_train_b @ best_theta

# Plotting the training points with the fitted line
plt.figure(figsize=(10, 6))
plt.scatter(x_train, y_train, color='blue', label='Training Data')
plt.plot(x_train, y_train_pred, color='red', label=f'Fitted Line (Learning Rate = {best_learning_rate})')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Training Data with Fitted Line (Gradient Descent)')
plt.legend()
plt.show()

# 3.1.2

# Defining the Polynomial Regression Class
class PolynomialRegression:
    def __init__(self, degree):
        self.degree = degree
        self.coefficients = None

    def fit(self, X, y):
        X_poly = self._generate_polynomial_features(X)
        X_poly_b = np.c_[np.ones((X_poly.shape[0], 1)), X_poly]
        self.coefficients = np.linalg.pinv(X_poly_b) @ y

    def predict(self, X):
        X_poly = self._generate_polynomial_features(X)
        X_poly_b = np.c_[np.ones((X_poly.shape[0], 1)), X_poly]
        return X_poly_b @ self.coefficients

    def _generate_polynomial_features(self, X):
        # Generate polynomial features up to the specified degree
        return np.vstack([X**i for i in range(1, self.degree + 1)]).T


def standard_deviation(y):
    return np.std(y)

# Testing polynomial regression with various degrees
degrees = [1, 2, 3, 4, 5]
best_degree = None
best_mse = float('inf')
best_model = None

x_range = np.linspace(min(x_train), max(x_train), 100)

for degree in degrees:
    model = PolynomialRegression(degree)
    model.fit(x_train, y_train)
    
    y_train_pred = model.predict(x_train)
    y_test_pred = model.predict(x_test)
    
    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse = mean_squared_error(y_test, y_test_pred)
    train_std = standard_deviation(y_train_pred)
    test_std = standard_deviation(y_test_pred)
    train_var = variance(y_train_pred)
    test_var = variance(y_test_pred)
    
    print(f"Degree: {degree}")
    print(f"Training MSE: {train_mse}")
    print(f"Testing MSE: {test_mse}")
    print(f"Training Standard Deviation: {train_std}")
    print(f"Testing Standard Deviation: {test_std}")
    print(f"Training Variance: {train_var}")
    print(f"Testing Variance: {test_var}\n")
    
    y_range = model.predict(x_range)

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    #Original data and fitting line
    plt.subplot(2, 2, 1)
    plt.scatter(x_train, y_train, color='blue', label='Training Data', alpha=0.6)
    plt.plot(x_range, y_range, label=f'Degree {degree}', color='red')
    plt.title(f'Polynomial Degree {degree}')
    plt.legend()
    plt.grid(True)

    #MSE
    plt.subplot(2, 2, 2)
    plt.bar(['Train MSE', 'Test MSE'], [train_mse, test_mse], color=['#2ca02c', '#d62728'])
    plt.title('Mean Squared Error')
    plt.grid(True)

    #Standard Deviation
    plt.subplot(2, 2, 3)
    plt.bar(['Train Std Dev', 'Test Std Dev'], [train_std, test_std], color=['#9467bd', '#8c564b'])
    plt.title('Standard Deviation')
    plt.grid(True)

    #Variance
    plt.subplot(2, 2, 4)
    plt.bar(['Train Variance', 'Test Variance'], [train_var, test_var], color=['#17becf', '#bcbd22'])
    plt.title('Variance')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    
     # best degree based on the lowest test MSE
    if test_mse < best_mse:
        best_mse = test_mse
        best_degree = degree

# Plotting the final polynomial regression curves for all degrees
plt.figure(figsize=(10, 8))
for degree in degrees:
    model = PolynomialRegression(degree)
    model.fit(x_train, y_train)
    y_range = model.predict(x_range)
    plt.plot(x_range, y_range, label=f'Degree {degree}')

# Plotting the data points and final regression curves
plt.scatter(x_train, y_train, color='blue', label='Training Data', alpha=0.6)
plt.scatter(x_test, y_test, color='green', label='Testing Data', alpha=0.6)
plt.scatter(x_val, y_val, color='red', label='Validation Data', alpha=0.6)
plt.title('Polynomial Regression Curves for Different Degrees')
plt.xlabel('x (Independent Variable)')
plt.ylabel('y (Dependent Variable)')
plt.legend()
plt.grid(True)
plt.show()

print(f"Best Degree: {best_degree}, Best Testing MSE: {best_mse}")

