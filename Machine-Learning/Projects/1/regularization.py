import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt('C:/Users/Affan/Desktop/python/regularisation.csv', delimiter=',', skip_header=1)

np.random.shuffle(data)

train_size = int(0.8 * len(data))
val_size = int(0.1 * len(data))
train_data = data[:train_size]
val_data = data[train_size:train_size + val_size]
test_data = data[train_size + val_size:]

x_train, y_train = train_data[:, 0], train_data[:, 1]
x_val, y_val = val_data[:, 0], val_data[:, 1]
x_test, y_test = test_data[:, 0], test_data[:, 1]

plt.figure(figsize=(8, 6))
plt.scatter(x_train, y_train, color='blue', label='Training Data', alpha=0.6)
plt.title('Training Dataset Visualization')
plt.xlabel('x (Independent Variable)')
plt.ylabel('y (Dependent Variable)')
plt.legend()
plt.grid(True)
plt.show()


def polynomial_features(X, degree):
    return np.vstack([X**i for i in range(degree + 1)]).T

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


def gradient_descent(X, y, theta, learning_rate, n_iterations, l1_reg=0, l2_reg=0):
    m = len(y)
    for iteration in range(n_iterations):
        predictions = X @ theta
        errors = predictions - y
        gradients = (2/m) * (X.T @ errors + l1_reg * np.sign(theta) + l2_reg * theta)
        theta = theta - learning_rate * gradients
    return theta

def regularized_polynomial_regression(x_train, y_train, x_val, y_val, degree, l1_reg=0, l2_reg=0, learning_rate=0.01, n_iterations=1000):
    X_train_poly = polynomial_features(x_train, degree)
    X_val_poly = polynomial_features(x_val, degree)
    
    theta = np.zeros(X_train_poly.shape[1])
    
    theta = gradient_descent(X_train_poly, y_train, theta, learning_rate, n_iterations, l1_reg, l2_reg)
    
    y_train_pred = X_train_poly @ theta
    y_val_pred = X_val_poly @ theta
    
    mse_train = mean_squared_error(y_train, y_train_pred)
    mse_val = mean_squared_error(y_val, y_val_pred)
    
    return theta, mse_train, mse_val

# Testing different polynomial degrees and regularization
degrees = [1, 5, 10, 15, 20]
l1_reg = 0.1  # L1 regularization parameter
l2_reg = 0.1  # L2 regularization parameter

for degree in degrees:
    # Without regularization
    theta, mse_train, mse_val = regularized_polynomial_regression(x_train, y_train, x_val, y_val, degree)
    print(f"Degree: {degree}, MSE (Train): {mse_train:.4f}, MSE (Val): {mse_val:.4f} (No Regularization)")
    
    # With L1 regularization
    theta, mse_train, mse_val = regularized_polynomial_regression(x_train, y_train, x_val, y_val, degree, l1_reg=l1_reg)
    print(f"Degree: {degree}, MSE (Train): {mse_train:.4f}, MSE (Val): {mse_val:.4f} (L1 Regularization)")
    
    # With L2 regularization
    theta, mse_train, mse_val = regularized_polynomial_regression(x_train, y_train, x_val, y_val, degree, l2_reg=l2_reg)
    print(f"Degree: {degree}, MSE (Train): {mse_train:.4f}, MSE (Val): {mse_val:.4f} (L2 Regularization)")

# Visualizing results
x_range = np.linspace(min(x_train), max(x_train), 100)

plt.figure(figsize=(12, 8))
for degree in degrees:
    X_range_poly = polynomial_features(x_range, degree)
    
    # Without regularization
    theta, _, _ = regularized_polynomial_regression(x_train, y_train, x_val, y_val, degree)
    y_range = X_range_poly @ theta
    plt.plot(x_range, y_range, label=f'Degree {degree} (No Regularization)')
    
    # With L1 regularization
    theta, _, _ = regularized_polynomial_regression(x_train, y_train, x_val, y_val, degree, l1_reg=l1_reg)
    y_range = X_range_poly @ theta
    plt.plot(x_range, y_range, '--', label=f'Degree {degree} (L1 Regularization)')
    
    # With L2 regularization
    theta, _, _ = regularized_polynomial_regression(x_train, y_train, x_val, y_val, degree, l2_reg=l2_reg)
    y_range = X_range_poly @ theta
    plt.plot(x_range, y_range, ':', label=f'Degree {degree} (L2 Regularization)')

plt.scatter(x_train, y_train, color='blue', label='Training Data', alpha=0.6)
plt.title('Polynomial Regression with Regularization')
plt.xlabel('x (Independent Variable)')
plt.ylabel('y (Dependent Variable)')
plt.legend()
plt.grid(True)
plt.show()
