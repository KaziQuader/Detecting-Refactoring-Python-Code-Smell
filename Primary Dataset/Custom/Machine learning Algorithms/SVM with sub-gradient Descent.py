import numpy as np
import random
import math

class SVM:
  def __init__(self, weights, x, y, lambd, alpha, epoch):
    self.weights = weights
    self.x = x
    self.y = y
    self.lambd = lambd
    self.alpha = alpha
    self.epoch = epoch
    self.error = []

  def sub_gradient_descent(self):
    min_error = math.inf

    for i in range(self.epoch):
      random_data = random.randint(0, len(self.x) - 1)
      
      y_k = self.y[random_data]
      dot_weight_x_k = np.dot(self.weights, self.x[random_data])

      for j in range(len(self.x[random_data])):
        if 1 > y_k * dot_weight_x_k:
          self.weights[j] = ((1 - self.lambd)*self.weights[j]) + (self.alpha * self.lambd * len(self.x) * y_k * self.x[random_data][j])
        else:
          self.weights[j] = (1 - self.lambd) * self.weights[j]

      error = (1/2 * np.dot(self.weights, self.weights)) + ((self.alpha * len(self.x)) * max(0, 1 - (y_k*dot_weight_x_k)))
 
      if error < min_error:
        min_error = error
        
      if i == 0:
        print("Max Error:", error)
        print("Weights for Max Error:", self.weights)
        print("---------------------------------------")

      self.error.append(error)

    print("Min Error:", min_error)
    print("Weights for Min Error:", self.weights)
    print("---------------------------------------")


  def print_errors(self):
    print("Errors at every 100th interval")
    for i in range(len(self.error)):
      if  i % 100 == 0:
        print(f"Error at {i}th interval: {self.error[i]}")
    


# Dataset Generation
def function(x):
  val = -13 * x[0] + 2001 * x[1] - 20 * x[2] + 41 * x[3] - x[4]
  if val >= 0:
    return 1
  else:
    return -1

n = 5
m = 1000

x = []
y = []

for i in range(m):
  a = []
  for j in range(n):
    a.append(np.random.randint(-100,100))

  x.append(a)
  y.append(function(a))

w = np.zeros(n)
lambd = 0.1
alpha = 0.01
epoch = 1000

model = SVM(w, x, y, lambd, alpha, epoch)
model.sub_gradient_descent()
model.print_errors()