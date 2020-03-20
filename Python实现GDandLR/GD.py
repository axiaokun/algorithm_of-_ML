import numpy as np
from sklearn.datasets import load_boston
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

class SGD_simple():

    def __init__(self, eta=0.01, n_iterations=50000, epsilon=1e-5):
        self.eta = eta
        self.n_iterations = n_iterations
        self.epsilon = epsilon
        self.fit_theta = None
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        iteration = 0
        loss = 1
        y = y.reshape((len(y), 1))
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        theta = np.random.rand(X_b.shape[1], 1)
        sample = X_b.shape[0]
        while iteration < self.n_iterations and loss > self.epsilon:
            last_theta = theta
            iteration += 1
            random_index = np.random.randint(sample)
            X_i = X_b[random_index:random_index+1]
            y_i = y[random_index:random_index+1]
            gradients = 2 * X_i.T.dot(X_i.dot(theta) - y_i)
            theta = theta - self.eta * gradients
            loss = np.linalg.norm(theta - last_theta)
        self.fit_theta = theta
        self.coef_ = theta[1:].reshape(X.shape[1])
        self.intercept_ = theta[:1].reshape(1)
        print(iteration)

    def predict(self, X_i):
        X_b = np.c_[np.ones((X_i.shape[0], 1)), X_i]
        return X_b.dot(self.fit_theta)

class BGD_simple():

    def __init__(self, eta=0.01, n_iterations=10000, epsilon=1e-5):
        self.eta = eta
        self.n_iterations = n_iterations
        self.epsilon = epsilon
        self.fit_theta = None
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        iteration = 0
        loss = 1
        y = y.reshape((len(y), 1))
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        theta = np.random.rand(X_b.shape[1], 1)
        sample = X_b.shape[0]
        while iteration < self.n_iterations and loss > self.epsilon:
            last_theta = theta
            iteration += 1
            gradients = 2/sample * X_b.T.dot(X_b.dot(theta) - y)
            theta = theta - self.eta * gradients
            loss = np.linalg.norm(theta - last_theta)
        self.fit_theta = theta
        self.coef_ = theta[1:].reshape(X.shape[1])
        self.intercept_ = theta[:1].reshape(1)
        print(iteration)

    def predict(self, X_i):
        X_b = np.c_[np.ones((X_i.shape[0], 1)), X_i]
        return X_b.dot(self.fit_theta)

class MBGD_simple():

    def __init__(self, eta=0.01, n_iterations=10000, epsilon=1e-5, batch_size=2):
        self.eta = eta
        self.n_iterations = n_iterations
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.fit_theta = None
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        iteration = 0
        loss = 1
        y = y.reshape((len(y), 1))
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        theta = np.random.rand(X_b.shape[1], 1)
        sample = X_b.shape[0]
        while iteration < self.n_iterations and loss > self.epsilon:
            last_theta = theta
            iteration += 1
            i = np.random.randint(sample)
            i_batch_size = (i + self.batch_size) % (sample)
            if i + self.batch_size > sample-1:
                for j in range(i, sample):
                    X_i = X_b[j: j + 1]
                    y_i = y[j: j + 1]
                    gradients = 2 * X_i.T.dot(X_i.dot(theta) - y_i)
                    theta = theta - self.eta * gradients
                for j in range(i_batch_size):
                    X_i = X_b[j: j + 1]
                    y_i = y[j: j + 1]
                    gradients = 2 * X_i.T.dot(X_i.dot(theta) - y_i)
                    theta = theta - self.eta * gradients
            else:
                for j in range(i, i_batch_size):
                    X_i = X_b[j: j + 1]
                    y_i = y[j: j + 1]
                    gradients = 2 * X_i.T.dot(X_i.dot(theta) - y_i)
                    theta = theta - self.eta * gradients
            loss = np.linalg.norm(theta - last_theta)
        self.fit_theta = theta
        self.coef_ = theta[1:].reshape(X.shape[1])
        self.intercept_ = theta[:1].reshape(1)
        print(iteration)
        print(loss)

    def predict(self, X_i):
        X_b = np.c_[np.ones((X_i.shape[0], 1)), X_i]
        return X_b.dot(self.fit_theta)

class LinearRegression_simple():

    def __init__(self):
        self.coef_ = None
        self.intercept_ = None
        self.fit_theta = None

    def fit(self, X, y):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        y = y.reshape(len(y), 1)
        self.fit_theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
        self.coef_ = self.fit_theta[1:].reshape(X.shape[1])
        self.intercept_ = self.fit_theta[0].reshape(1)

    def predict(self, X_i):
        X_b = np.c_[np.ones((X_i.shape[0]), 1), X_i]
        return X_b.dot(self.fit_theta)

if __name__ == "__main__":
    boston = load_boston()
    X = boston['data']
    y = boston['target']
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    BGD = MBGD_simple()
    SGD2 = SGDRegressor()
    BGD.fit(X, y)
    SGD2.fit(X, y)
    print(BGD.intercept_, BGD.coef_)
    print(SGD2.intercept_, SGD2.coef_)