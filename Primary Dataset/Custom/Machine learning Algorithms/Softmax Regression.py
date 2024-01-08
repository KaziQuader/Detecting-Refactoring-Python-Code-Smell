import torch
import torchvision
import torch.nn as nn
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np


train_dataset = torchvision.datasets.FashionMNIST(root = '', train = True, transform = transforms.ToTensor(), download = True)
test_dataset = torchvision.datasets.FashionMNIST(root = '', train = False, transform = transforms.ToTensor(), download = True)

train_loader = torch.utils.data.DataLoader(dataset = train_dataset, batch_size = 100, shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset = test_dataset, batch_size = 100, shuffle = False)

examples = iter(train_loader)
samples, labels = next(examples)
print(samples.shape)
print(labels.shape)

for i in range(8):
  plt.subplot(2, 4, i+1)
  plt.imshow(samples[i][0], cmap = 'viridis')

plt.show()


# Initialize weights and biases
weights = np.random.rand(784, 10)
biases = np.random.rand(10)
lambd = 0.01

# loop for 20 epochs:
for epoch in range(20):
  for i, (images, labels) in enumerate(train_loader): # batch loop

      images = images.reshape(-1, 28*28)  #contains 100 images per batch with dimension 1*784
      # print("Images", images)

      scores = np.dot(images.numpy(), weights) + biases
      # print("Scores", scores)

      scores_k = np.exp(scores)
      scores_l = np.sum(np.exp(scores_k))
      # print("Scores_K", scores_k)
      # print("Scores_L", scores_l)


      labels_encoded = np.eye(10)[labels]
      weight_error = (scores_k / scores_l) - labels_encoded
      bias_error = (scores_k / scores_l) - labels_encoded

      weight_descent = np.dot(images.T.numpy(), weight_error)
      bias_descent = np.sum(bias_error)

      weights = weights - (lambd * weight_descent)
      biases = biases - (lambd * bias_descent)

print(weights)
print(biases)






