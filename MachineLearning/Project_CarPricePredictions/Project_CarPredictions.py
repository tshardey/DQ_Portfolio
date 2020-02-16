
# coding: utf-8

# # Predicting Market Price for a Car
# 
# The Automobile Datatset was obtained from UCL's Machine Learning Repository. 
# 
# The data set contains information on: the specification of the car, the assigned insurance risk and the normalized losses in use when compared to other cars.  
# 
# ## Source
# 
# 1) 1985 Model Import Car and Truck Specifications, 1985 Ward's Automotive Yearbook. 
# 
# 2) Personal Auto Manuals, Insurance Services Office, 160 Water Street, New York, NY 10038 
# 
# 3) Insurance Collision Report, Insurance Institute for Highway Safety, Watergate 600, Washington, DC 20037
# 
# Creator/Donor: 
# 
# Jeffrey C. Schlimmer 
# 

# In[62]:


import pandas as pd
import numpy as np


# In[63]:


# Importing the data
cars = pd.read_table("imports-85.data", delimiter=',', header=None)
# Assigning column names
column_names =['symboling','normalized_losses', 'make', 'fuel_type', 'aspiration', 'num_doors', 'body_style', 'drive_wheels', 'engine_location', 'wheel_base', 'length', 'width', 'height', 'curb_weight', 'engine_type', 'num_cylinders', 'engine_size', 'fuel_system', 'bore', 'stroke', 'compression_ratio', 'horsepower', 'peak_rpm', 'city_mpg', 'highway_mpg', 'price']
cars.columns = column_names

cars.info()


# ## Potential Features 
# 
# The following are all numeric type and do not have null entries so they might make good featrure columns. 
# 
# - symboling            205 non-null int64
# - wheel_base           205 non-null float64
# - length               205 non-null float64
# - width                205 non-null float64
# - height               205 non-null float64
# - curb_weight          205 non-null int64
# - engine_size          205 non-null int64
# - compression_ratio    205 non-null float64
# - city_mpg             205 non-null int64
# - highway_mpg          205 non-null int64
# 
# Normalized-losess appears to be an int type object but the presence of blank values, listed as "?" has caused it to be classified as an object type.  This could be an issue with more columns. 

# In[64]:


cars.head()


# In[65]:


# Replacing all of the "?" with null values
cars.replace("?", np.nan, inplace=True)


# In[66]:


# Determining which columns were affected by the replacement
cars.info()


# In[67]:


# Subsetting the dataset to include only those with continious values
continuous_values_cols = ['normalized_losses', 'wheel_base', 'length', 'width', 'height', 'curb_weight', 'bore', 'stroke', 'compression_ratio', 'horsepower', 'peak_rpm', 'city_mpg', 'highway_mpg', 'price']
numeric_cars = cars[continuous_values_cols].copy()
numeric_cars.head()


# In[68]:


# Changing all columns to type 'float'
numeric_cars = numeric_cars.astype('float')
numeric_cars.isnull().sum()


# In[69]:


# Looking at null price values
numeric_cars[numeric_cars['price'].isna()]


# Since the price is what we want to predict, the rows containing null values will be dropped. 

# In[70]:


# Dropping NA values for price
numeric_cars = numeric_cars.dropna(subset=['price'])


# In[71]:


# Looking at normalized losses
print("The normalized losses range is: {}".format([numeric_cars['normalized_losses'].min(), numeric_cars['normalized_losses'].max()]))
print("The normalized losses mean is: {}".format(numeric_cars['normalized_losses'].mean()))


# For the remaining rows, the average will be used to replace all null values in order to leave the columns into determine significance. 

# In[72]:


# Replace missing values in other columns using column means.
numeric_cars = numeric_cars.fillna(numeric_cars.mean())
numeric_cars.info()


# In[73]:


# Normalize all columnns to range from 0 to 1 except the target column.
price_col = numeric_cars['price']
numeric_cars = (numeric_cars - numeric_cars.min())/(numeric_cars.max() - numeric_cars.min())
numeric_cars['price'] = price_col


# In[74]:


# Creating a k-nearest neighbor train and test function
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

def knn_train_test(train_col, target_col, df):
    knn = KNeighborsRegressor()
    np.random.seed(1)
        
    # Randomize order of rows in data frame.
    shuffled_index = np.random.permutation(df.index)
    rand_df = df.reindex(shuffled_index)

    # Divide number of rows in half and round.
    last_train_row = int(len(rand_df) / 2)
    
    # Select the first half and set as training set.
    # Select the second half and set as test set.
    train_df = rand_df.iloc[0:last_train_row]
    test_df = rand_df.iloc[last_train_row:]
    
    # Fit a KNN model using default k value.
    knn.fit(train_df[[train_col]], train_df[target_col])
    
    # Make predictions using model.
    predicted_labels = knn.predict(test_df[[train_col]])

    # Calculate and return RMSE.
    mse = mean_squared_error(test_df[target_col], predicted_labels)
    rmse = np.sqrt(mse)
    return rmse


# In[75]:


# Getting the column names
column_names = numeric_cars.columns.drop('price')
# Empty dictionary to house the rmse and corresponding column
train_col_dict = {}

for column in column_names:
    train_col_dict[column] = knn_train_test(column, 'price', numeric_cars)
    
train_col_ser = pd.Series(train_col_dict).sort_values()
train_col_ser


# ## Feature Optimization

# In[76]:


def knn_train_test(train_col, target_col, df, k=5):
    np.random.seed(1)
        
    # Randomize order of rows in data frame.
    shuffled_index = np.random.permutation(df.index)
    rand_df = df.reindex(shuffled_index)

    # Divide number of rows in half and round.
    last_train_row = int(len(rand_df) / 2)
    
    # Select the first half and set as training set.
    # Select the second half and set as test set.
    train_df = rand_df.iloc[0:last_train_row]
    test_df = rand_df.iloc[last_train_row:]
    
    # A list of k values to be evaluated
    k_values = [1, 3, 5, 7, 9]
    k_feat_dict = {}
    
    for k in k_values:
        knn = KNeighborsRegressor(n_neighbors = k)
        # Fit a KNN model using selected k value.
        knn.fit(train_df[[train_col]], train_df[target_col])
        # Make predictions using model.
        predicted_labels = knn.predict(test_df[[train_col]])

        # Calculate and return RMSE.
        mse = mean_squared_error(test_df[target_col], predicted_labels)
        rmse = np.sqrt(mse)
        k_feat_dict[k] = rmse
    return k_feat_dict


# In[77]:


import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

k_feat = {}

# Looping through each column with adjusted k values
for column in column_names:
    k_feat[column] = knn_train_test(column, 'price', numeric_cars)
k_feat


# In[78]:


# Plotting each of the numerical columns with the variation in the k value
for k,v in k_feat.items():
    x = sorted(list(v.keys()))
    y = sorted(list(v.values()))
    
    plt.plot(x,y, label = k)
    plt.xlabel('k value')
    plt.ylabel('RMSE')

plt.legend(bbox_to_anchor=(1.5, 1.05))
plt.show()


# In[79]:


def knn_train_test(train_cols, target_col, df, k=5):
    np.random.seed(1)
        
    # Randomize order of rows in data frame.
    shuffled_index = np.random.permutation(df.index)
    rand_df = df.reindex(shuffled_index)

    # Divide number of rows in half and round.
    last_train_row = int(len(rand_df) / 2)
    
    # Select the first half and set as training set.
    # Select the second half and set as test set.
    train_df = rand_df.iloc[0:last_train_row]
    test_df = rand_df.iloc[last_train_row:]
    
    knn = KNeighborsRegressor(n_neighbors = k)
    # Fit a KNN model using selected k value.
    knn.fit(train_df[train_cols], train_df[target_col])
    # Make predictions using model.
    predicted_labels = knn.predict(test_df[train_cols])

    # Calculate and return RMSE.
    mse = mean_squared_error(test_df[target_col], predicted_labels)
    rmse = np.sqrt(mse)
    return rmse


# In[80]:


# Selecting the top 5 features
top_5_feat = list(train_col_ser.head(6).index)

top_5_dict = {}

# Looking at the top features in aggregate
for i in range(1, len(top_5_feat)):
    # Adding a feature each time
    selected_feat = top_5_feat[0:i+1]
    name_string = "top_" + str(i+1)
    top_5_dict[name_string] = knn_train_test(selected_feat, 'price', numeric_cars)
    
top_5 = pd.Series(top_5_dict).sort_values() 
top_5


# ## K Optimization

# In[81]:


# Optimizing the k value for the highest performing models
top_2_cols = top_5_feat[0:2]

k_25 = list(range(1,26))
top_2_rmse = {}

for i in k_25:
    top_2_rmse[i] = knn_train_test(top_2_cols, 'price', numeric_cars, i)

top_2_s = pd.Series(top_2_rmse)
top_2_rmse


# In[82]:


# Optimizing the k value for the highest performing models
top_5_cols = top_5_feat[0:6]

k_25 = list(range(1,26))
top_5_rmse = {}

for i in k_25:
    top_5_rmse[i] = knn_train_test(top_5_cols, 'price', numeric_cars, i)

top_5_s = pd.Series(top_5_rmse)
top_5_rmse


# In[83]:


# Optimizing the k value for the highest performing models
top_4_cols = top_5_feat[0:5]

k_25 = list(range(1,26))
top_4_rmse = {}

for i in k_25:
    top_4_rmse[i] = knn_train_test(top_4_cols, 'price', numeric_cars, i)

top_4_s = pd.Series(top_4_rmse)
top_4_rmse


# In[84]:


# Merging the series created for each model into a single dataframe 
top_models = pd.concat([top_2_s, top_5_s, top_4_s], axis=1) 
top_models.columns=['top_2', 'top_5', 'top_4']
top_models.plot()
plt.xlabel('K-Value')
plt.ylabel('RMSE')
plt.show()


# The RMSEs gets higher as the K-value gets bigger.  The optimal K-value for each of the top performing models is 1 or 2. The model using the Top 4 features, with a K-value of 1 performed best.

# ## Looking at Cross-Validation 

# In[92]:


from sklearn.model_selection import KFold, cross_val_score

# Utilizing KFold and cross_val_score for more robust testing
def knn_train_test(train_cols, target_col, df, k=5, split=2):
    kf = KFold(n_splits=split, shuffle=True, random_state=1)
    
    knn = KNeighborsRegressor(n_neighbors = k)

    # Calculate and return RMSE.
    mses = cross_val_score(knn, df[train_cols], df[target_col], scoring="neg_mean_squared_error", cv=kf)
    rmse = np.sqrt(np.absolute(mses))
    return np.mean(rmse), np.std(rmse)


# In[98]:


# Looking at a K-fold of 5 with the best performing model and a K-value of 1
top_4_mean, top_4_std = knn_train_test(top_2_cols, 'price', numeric_cars, 1, 5)

print("The mean RMSE for the Top 4 Features is: {}".format(round(top_4_mean),2))
print("The standard deviation of the RMSE for the Top 4 Features is: {}".format(round(top_4_std),2))


# The cross validation resulted in a value that was very similar to the two-split method that was employeed initially.  
