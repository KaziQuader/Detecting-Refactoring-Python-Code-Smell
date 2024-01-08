import numpy as np
import pandas as pd
import category_encoders as ce
import random
from collections import Counter

class DecisionTree():
  def __init__(self, _X, _y, _attributes, map):
    self.X = _X
    self.y = _y
    self.attributes = _attributes
    self.decision = None
    self.dictionary = {}
    self.attribute_name = ""
    self.feature_map = map

  def standard_deviation(self, arr):
    # Find out how to calculate it. https://en.wikipedia.org/wiki/Standard_deviation
    count = len(arr)
    sum = 0
    numerator_sum_std = 0

    for num in arr:
      sum += num
    avg = sum / count

    for num in arr:
      numerator = (num - avg)**2
      numerator_sum_std += numerator

    std = (numerator_sum_std / count)**(1/2)
    return std

  def find_best_attribute(self):
    std = self.standard_deviation(self.y)
    std_reduction = 0
    best_attribute = None

    for attr in self.attributes:
        x_col = self.X[ : , self.feature_map[attr]]
        unique_labels = np.unique(x_col)
        weighted_std = 0
       
        for label in unique_labels:
          mask = self.X[ : , self.feature_map[attr]] == label
          std_label = self.standard_deviation(self.y[mask])
          weighted_std += (len(self.y[mask])/ (len(self.y))) * std_label

        std_reduction_of_arr = std - weighted_std
        if std_reduction_of_arr > std_reduction:
          std_reduction = std_reduction_of_arr
          best_attribute = attr

    return best_attribute

  def build(self):
    if len(self.y) <= 3 or (self.standard_deviation(self.y) / np.mean(self.y)) < 0.1:
        # Make it a leaf if the dataset size is small or CV is low
        self.decision = np.mean(self.y)
        return

    best_attribute = self.find_best_attribute()
    if best_attribute is not None:
        self.attribute_name = best_attribute

        # Split the dataset based on the best attribute
        x_col = self.X[:, self.feature_map[best_attribute]]
        unique_values = np.unique(x_col)

        for value in unique_values:
            mask = self.X[:, self.feature_map[best_attribute]] == value
            dataset_X = self.X[mask, :]
            dataset_y = self.y[mask]

            # Remove the best attribute from the list of attributes for the child tree
            child_attributes = [attr for attr in self.attributes if attr != best_attribute]

            # Create a child decision tree
            child_tree = DecisionTree(dataset_X, dataset_y, child_attributes, self.feature_map)
            # Recursively build the child tree
            child_tree.build()
            # Add the child tree to the dictionary
            self.dictionary[value] = child_tree

  def predict(self, x):
    if self.decision is not None:
            return self.decision

    attribute_value = x[self.attribute_name]

    if attribute_value in self.dictionary:
        return self.dictionary[attribute_value].predict(x)
    else:
        # Handle the case where the value is not found in the dictionary
        return None

  def print_the_tree(self, level):
    print(len(self.attributes))
    if self.decision is not None:
      print('The decision is : ', self.decision)
      return

    print('At level: ', level, self.attribute_name)
    for key in self.dictionary:
      self.dictionary[key].print_the_tree(level + 1)

data = pd.DataFrame({'Outlook': ['Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Sunny', 'Rainy', 'Overcast', 'Overcast', 'Sunny'],
                        'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
                        'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
                        'Windy': ['False', 'True', 'False', 'False', 'False', 'True', 'True', 'False', 'False', 'False', 'True', 'True', 'False', 'True'],
                        'Target': [25, 30, 46, 45, 52, 23, 43, 35, 38, 46, 48, 52, 44, 30]
                        })

# Seperating features and target. Features are stored in X and target is stored in y
X = data.drop(['Target'], axis=1)
y = data['Target']
print(X)
# Encoded the categorical variables
encoder = ce.OrdinalEncoder(cols=['Outlook', 'Temperature', 'Windy', 'Humidity'])
X_train = encoder.fit_transform(X)

X_train = X_train.to_numpy()
y_train = y.to_numpy()

avg_hours_played = np.mean(y_train)
residue = y_train - avg_hours_played
alpha = 0.1
iterations = 100
prediction = avg_hours_played
residue_prediction = []
attributes = ['Outlook', 'Temp', 'Humidity', 'Windy']
map = {'Outlook': 0, 'Temp':1, 'Humidity':2, 'Windy':3}

for iter in range(iterations):
    y = residue
    dt = DecisionTree(X_train, y_train, attributes, map)
    dt.build()
    
    for row in X:
       residue_prediction.append(dt.predict(row))

    predictions = prediction + alpha * residue_prediction
    residue = y_train - prediction

print(prediction)
print(np.mean((y_train - prediction) ** 2))