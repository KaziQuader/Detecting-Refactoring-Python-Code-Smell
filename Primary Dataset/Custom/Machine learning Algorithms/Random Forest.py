import numpy as np
import pandas as pd
import category_encoders as ce
import random
from collections import Counter

class Node:
    # A node consists of these values
    def __init__(self, feature=None, children=None, value=None):
        self.feature = feature
        self.children = children
        self.value = value
    
class DecisionTree:
    def __init__(self, max_depth=5, min_num_samples=2):
        # Hyperparametres (Changing this will change the decision tree)
        self.max_depth = max_depth
        self.min_num_samples = min_num_samples
        self.root = None

    def fit(self, x, y):
        self.root = self.grow_tree(x, y)
        return self.root

    # Recursice Function to Build the Tree 
    # Left subtree is built first then the Right subtree
    # At last the Root is returned
    # Function req: get_best_split, get_label, recursively call grow_tree
    def grow_tree(self, x, y, depth=0):
        num_samples, num_feats = x.shape
        num_labels = len(np.unique(y))

        # Check Stopping Criteria
        if (depth > self.max_depth or num_samples < self.min_num_samples or num_labels == 1):
            leaf_value = self.get_label(y)
            return Node(value=leaf_value)

        # Get Best Split
        best_feature = self.get_best_split(x, y, num_feats)
        if best_feature is None:
            leaf_value = self.get_label(y)
            return Node(value=leaf_value)

        # Create subtrees for each label in best feature
        children = []
        for label in np.unique(x[:, best_feature]):
            mask = x[:, best_feature] == label
            if(np.sum(mask) >= self.min_num_samples):
                child_tree = self.grow_tree(x[mask], y[mask], depth+1)
                children.append((child_tree, label))

        return Node(feature=best_feature, children=children)

    def get_label(self, y):
        unique_labels, counts = np.unique(y, return_counts=True)
        return unique_labels[np.argmax(counts)]

    def calculate_gini(self, y):
        _, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return 1 - np.sum(probs**2)


    def get_best_split(self, x, y, num_feats):
        best_feature = None
        best_weighted_gini = 2

        if x.shape[0] <= 1:
            return None

        for feat in range(num_feats):
            x_col = x[:, feat] # Contains all the rows of that specific column
            unique_labels = np.unique(x_col)
            weighted_gini = 0

            for label in unique_labels:
                mask = x[:, feat] == label
                gini_label = self.calculate_gini(y[mask])
                weighted_gini += (len(y[mask]))/(len(y)) * gini_label

            if weighted_gini < best_weighted_gini:
                best_weighted_gini = weighted_gini
                best_feature = feat

        return best_feature
    
    def print(self, root, features):
        if root is None:
            return
        
        queue = []
        queue.append(root)
        level = 1
        i = 0

        while len(queue) > 0:
            if i == 0:
                if queue[0].feature is not None:
                    print(f"Level {level}: {features[queue[0].feature]}")
                node = queue.pop(0)
                level += 1
                i += 1

                if node.children is not None:
                    queue.append(node.children)

            else:
                for feat, label in queue[0]:
                    if feat.children is not None:
                        print(f"Level {level}: {features[feat.feature]}")
                level += 1

                node = queue.pop(0)
                for i, j in node:
                    if i.children is not None:
                        queue.append(i.children)
            
    def predict(self, root, x, features):
        node = root
        i = 0
        while True:
            if node.value is not None:
                return node.value
            
            if features[i] == features[node.feature]:
                for child, label in node.children:
                    if label == x[i]:
                        node = child
                        i = 0
            else:
                i += 1
            
        return node.value
    
class RandomForest:
    def __init__(self, n_estimators):
        self.n_estimators = n_estimators
        self.trees = []

    def fit(self, x, y):
        bootstrap_dataset_x, bootstrap_dataset_y = self.create_bootstrap_dataset(x, y)
        random_x_cols = self.get_random_columns(bootstrap_dataset_x)
        for i in range(self.n_estimators):
            tree = DecisionTree()
            root = tree.fit(random_x_cols, bootstrap_dataset_y)
            self.trees.append((tree, root))

    def create_bootstrap_dataset(self, x, y):
        random_rows = np.random.choice(x.shape[0], x.shape[0], replace=False)
        return x[random_rows], y[random_rows]
    
    def get_random_columns(self, bootstrap_dataset_x):
        random_nums = random.randint(0, bootstrap_dataset_x.shape[1])
        random_cols = np.random.choice(bootstrap_dataset_x.shape[1], random_nums, replace=False)
        return bootstrap_dataset_x[:, random_cols]
    
    def predict(self, x, features):
        predictions = []
        for tree, root in self.trees:
            prediction = tree.predict(root, x, features)
            predictions.append(prediction)

        elements_count = Counter(predictions)
        return elements_count.most_common(1)[0][0]

# Creating the data frame
data = pd.DataFrame({'Outlook': ['Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Sunny', 'Rainy', 'Overcast', 'Overcast', 'Sunny'],
                        'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
                        'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
                        'Windy': ['False', 'True', 'False', 'False', 'False', 'True', 'True', 'False', 'False', 'False', 'True', 'True', 'False', 'True'],
                        'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
                        })



# Seperating features and target. Features are stored in X and target is stored in y
X = data.drop(['Play'], axis=1)
y = data['Play']
# Encoded the categorical variables
encoder = ce.OrdinalEncoder(cols=['Outlook', 'Temperature', 'Windy', 'Humidity'])
tencoder = ce.OrdinalEncoder(cols = ['Play'])
X_train = encoder.fit_transform(X)
y_train = tencoder.fit_transform(y)

# Converted dataframe
X_train = X_train.to_numpy()
y_train = y_train.to_numpy()

# Getting the column names
features = X.columns.tolist()

# Decision Tree
tree = DecisionTree()
root = tree.fit(X_train , y_train)
tree.print(root, features)
print("Prediction:", tree.predict(root, [1, 1, 1, 1], features))

forest = RandomForest(5)
forest.fit(X_train, y_train)
print("Prediction:", forest.predict([1,1,1,1], features))

# print(y_train)
# print(X_train)
# print(X_train[:, 0] == 1)
# print(y_train[X_train[:, 0] == 1])
# print(X_train[X_train[:, 0] == 1])
# un, count = np.unique(y_train[X_train[:, 0] == 1], return_counts=True)
# print(un, count)
# counts = [3,4]
# print(np.argmax(counts))
# print(tree, root)
# print(X_train.shape)
# bootstrap = np.random.choice(X_train.shape[0], X_train.shape[0], replace=False)
# print(bootstrap)
# d = X_train[bootstrap]