import numpy as np

class LinearRegression:
  def __init__(self, lamb, iter, x, y, w, b, type, alpha):
    self.lambd = lamb
    self.iter = iter
    self.x_train = x
    self.y_train = y
    self.w = w
    self.b = b
    self.type = type
    self.alpha = alpha

  def compute_cost(self):
    MSE = 0.0
    m = self.x_train.shape[0]

    for i in range(m):
      h_w = np.dot(self.x_train[i], self.w) + self.b
      MSE = MSE + (self.y_train[i] - h_w)**2

    cost = MSE
    if self.type == "Ridge":
      square = self.w ** 2
      sum_of_square = np.sum(square)
      ridge_term = self.alpha * sum_of_square
      cost = MSE + ridge_term
    elif self.type == "Lasso":
      sum_of_modulus = np.sum(np.abs(self.w))
      lasso_term = self.alpha * sum_of_modulus
      cost = MSE + lasso_term
    else:
      cost = MSE

    return cost / m
  
  def compute_gradient(self):
    m, n = self.x_train.shape
    dj_dw = np.zeros((n,))
    dj_db = 0.0

    for i in range(m):
      err = self.y_train[i] - np.dot(self.x_train[i], self.w) + self.b

      for j in range(n):
        dj_dw[j] = dj_dw[j] + 2 * err * -self.x_train[i, j]

        if self.type == "Ridge":
          dj_dw[j] += 2 * self.alpha * self.w[j]
        elif self.type == "Lasso":
          dj_dw[j] += self.alpha * np.sign(self.w[j])

      dj_db = dj_db + (2 * err * -1)

      dj_db = dj_db / m
      dj_dw = dj_dw / m

    return dj_db, dj_dw
  
  def gradient_descent(self):
    cost_history = []
    cost_history.append(self.compute_cost())

    for i in range(self.iter):
      dj_db, dj_dw = self.compute_gradient()

      self.w = self.w - self.lambd * dj_dw
      self.b = self.b - self.lambd * dj_db

      if i % 100 == 0:
        cost_history.append(self.compute_cost())

    print(cost_history)

def f(x):
  return 100*x[2] - 17*x[1] + 3*x[0] + 11

def generate(a, b, mean, std, shape):
  x = np.random.uniform(a, b, shape) # takes 'size' number of random values from the range [a, b]
  y = [f(a) for a in x] # for each x, calculates f(x)
  noise = np.random.normal(mean, std, shape[0]) # for each x, calculates some noise
  y = y + noise # adds the noise to f(x)
  y = np.array(y)
  return x, y

training_size = 1000
features = 3
train_x, train_y = generate(-1, 1, 0, 0.1, (training_size, features))

initial_w = np.array([100, -17, 3])
initial_b = 11
iterations = 1000
lamb = 0.001
alpha = 0.01

linear_regression = LinearRegression(lamb, iterations, train_x, train_y, initial_w, initial_b, "Simple", alpha)
linear_regression.gradient_descent()
print(linear_regression.w, linear_regression.b)