#!/usr/bin/env python
# coding: utf-8

# # Handwritten Digit Classifier
# 
# Complications with image classification:
# - Each image is high dimensional 
# - Images are often downsampled to lower resolations or transformed to grayscale
# - Features from images don't have an obvious linear or nonlinear relationship
# 
# Exploring the effectiveness of deep, feedforward neural networks at classifying images.

# In[128]:


from sklearn.datasets import load_digits
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
get_ipython().magic('matplotlib inline')


# In[129]:


digits = load_digits()
print(digits.data.shape)


# ## Previewing the Data

# In[130]:


# Loading the data into a dataframe
digits_df = pd.DataFrame(digits.data)
digit_target = pd.Series(digits.target)

# Looking at the first row (image)
first_image =  digits_df.iloc[0]
np_image = first_image.values
# Reshaping to an 8x8 grid
np_image = np_image.reshape(8, 8)
plt.imshow(np_image, cmap='gray_r')


# In[131]:


digits_df = pd.concat([digits_df, digit_target], axis=1)


# In[132]:


def display_image(row):
    # Looking at the specified row (image)
    first_image =  digits_df.iloc[row, :64]
    np_image = first_image.values
    # Reshaping to an 8x8 grid
    np_image = np_image.reshape(8, 8)
    plt.imshow(np_image, cmap='gray_r') 


# In[133]:


fig, axes = plt.subplots(2, 4, figsize = (12,4))

rows = [0, 100, 200, 300, 1000, 1100, 1200, 1300]

for i in range(8):
    ax = fig.add_subplot(2,4,i+1)
    display_image(rows[i])


# ## Testing K-Nearest Neighbor

# In[134]:


# Function to split the data into train and test 
def split_data(df, split=0.7, seed=1):
    np.random.seed(seed)
    df_shuffled = df.iloc[np.random.permutation(len(df))]
    train = df_shuffled[:int(len(df)*split)]
    test = df_shuffled[int(len(df)*split):]
    return train, test


# In[135]:


# Function to train the model
def train_model(train_X, train_y, k=5):
    knn = KNeighborsClassifier(n_neighbors=k)
    model = knn.fit(train_X, train_y)
    return model


# In[108]:


# Function to test the model
def test_model(test_X, test_y, model):
    predictions = model.predict(test_X)
    accuracy = accuracy_score(test_y, predictions)
    return accuracy


# In[110]:


train, test = split_data(digits_df)
train_X = train.iloc[:, :64]
train_y = train.iloc[:, 64]
test_X = test.iloc[:, :64]
test_y = test.iloc[:, 64]

model = train_model(train_X, train_y)

accuracy = test_model(test_X, test_y, model)
print(accuracy)


# In[112]:


# Function to cross validate the model 
def cross_validate(cv, k=5):
    accuracy = []
    for i in range(cv):
        train, test = split_data(digits_df, 0.8, i)
        train_X = train.iloc[:, :64]
        train_y = train.iloc[:, 64]
        test_X = test.iloc[:, :64]
        test_y = test.iloc[:, 64]
        model = train_model(train_X, train_y, k)
        accuracy.append(test_model(test_X, test_y, model))
    return np.mean(accuracy)


# In[114]:


# Looking at different k values for k nearest neighbors
k_values = range(1, 21)

k_accuracy = {}

for k in k_values:
    k_accuracy[k] = cross_validate(4, k)


# In[116]:


plt.style.use('ggplot')
pd.Series(k_accuracy).plot()
plt.xlabel('k values')
plt.ylabel('accuracy')
plt.show()


# ## Looking at MLP Classifier

# In[124]:


neurons  = [8, 16, 32, 64, 128, 256]

# Function to train the model
def train_model_mlg(train_X, train_y, n=10):
    mlp = MLPClassifier(hidden_layer_sizes=(n,))
    model = mlp.fit(train_X, train_y)
    return model

# Function to cross validate the model 
def cross_validate_mlg(cv=4, n=100):
    accuracy = []
    for i in range(cv):
        train, test = split_data(digits_df, 0.8, i)
        train_X = train.iloc[:, :64]
        train_y = train.iloc[:, 64]
        test_X = test.iloc[:, :64]
        test_y = test.iloc[:, 64]
        model = train_model_mlg(train_X, train_y, n)
        accuracy.append(test_model(test_X, test_y, model))
    return np.mean(accuracy)


# In[120]:


train, test = split_data(digits_df)
train_X = train.iloc[:, :64]
train_y = train.iloc[:, 64]
test_X = test.iloc[:, :64]
test_y = test.iloc[:, 64]

model = train_model_mlg(train_X, train_y)

accuracy = test_model(test_X, test_y, model)
print(accuracy)


# In[ ]:


n_accuracy = {}

for n in neurons:
    n_accuracy[n] = cross_validate_mlg(4, n)
    
pd.Series(n_accuracy).plot()
plt.xlabel('neuron values')
plt.ylabel('accuracy')
plt.show()


# ## Two hidden layers

# In[ ]:


# Function to train the model
def train_model_mlg2(train_X, train_y, n=100):
    mlp = MLPClassifier(hidden_layer_sizes=(n, n))
    model = mlp.fit(train_X, train_y)
    return model

# Function to cross validate the model 
def cross_validate_mlg2(cv=4, n=100):
    accuracy = []
    for i in range(cv):
        train, test = split_data(digits_df, 0.8, i)
        train_X = train.iloc[:, :64]
        train_y = train.iloc[:, 64]
        test_X = test.iloc[:, :64]
        test_y = test.iloc[:, 64]
        model = train_model_mlg2(train_X, train_y, n)
        accuracy.append(test_model(test_X, test_y, model))
    return np.mean(accuracy)

n_accuracy2 = {} 
for n in [64, 128]:
    n_accuracy2[n] = cross_validate_mlg2(4, n)
    
pd.Series(n_accuracy2).plot()
plt.xlabel('neuron values')
plt.ylabel('accuracy')
plt.show()


# ## Three hidden layers

# In[ ]:


# Function to train the model
def train_model_mlg3(train_X, train_y, n=100):
    mlp = MLPClassifier(hidden_layer_sizes=(n, n, n))
    model = mlp.fit(train_X, train_y)
    return model

# Function to cross validate the model 
def cross_validate_mlg3(cv=4, n=100):
    accuracy = []
    for i in range(cv):
        train, test = split_data(digits_df, 0.8, i)
        train_X = train.iloc[:, :64]
        train_y = train.iloc[:, 64]
        test_X = test.iloc[:, :64]
        test_y = test.iloc[:, 64]
        model = train_model_mlg3(train_X, train_y, n)
        accuracy.append(test_model(test_X, test_y, model))
    return np.mean(accuracy)

n_accuracy3 = {} 
for n in [10, 64, 128]:
    n_accuracy3[n] = cross_validate_mlg3(4, n)
    
pd.Series(n_accuracy3).plot()
plt.xlabel('neuron values')
plt.ylabel('accuracy')
plt.show()


# In[ ]:




