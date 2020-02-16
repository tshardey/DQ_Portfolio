import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Reading in the csv file
sphist = pd.read_csv("sphist.csv")
# Converting the "Date" column to a datetime object
sphist['Date'] = pd.to_datetime(sphist['Date'])
# Sorting the dataframe by the date
sphist.sort_values(by ='Date', ascending=True, inplace=True)
# Selecting the columns of importance
sphist_close = sphist[['Date', 'Close']].copy().reset_index()
# Function to create a five day rolling average
def five_day_avg(df):
    avg_per_5 = pd.Series()
    for idx, row in df.iterrows():
        if idx >= 5:
            avg_per_5.loc[idx] = df.iloc[idx-5:idx,2].mean()
        else:
            avg_per_5.loc[idx] = 0
    return avg_per_5
# Function to create a five day rolling standard deviation
def thirty_day_std(df):
    std_per_30 = pd.Series()
    for idx, row in df.iterrows():
        if idx >= 30:
            std_per_30.loc[idx] = df.iloc[idx-30:idx,2].std()
        else:
            std_per_30.loc[idx] = 0
    return std_per_30
# Function to create a yearly rolling average
def year_avg(df):
    avg_per_365 = pd.Series()
    for idx, row in df.iterrows():
        if idx < 365:
            avg_per_365.loc[idx] = 0
        else: 
            end_date = row['Date']
            start_date = row['Date'] - timedelta(days=365)
            avg_per_365.loc[idx] = df[df['Date'].between(start_date, end_date, inclusive=False)]['Close'].mean()
    return avg_per_365

# Function to calculate a five day volume
def five_day_vol(df):
    vol_per_5 = pd.Series()
    for idx, row in df.iterrows():
        if idx >= 5:
            vol_per_5.loc[idx] = df.iloc[idx-5:idx,2].sum()/5
        else:
            vol_per_5.loc[idx] = 0
    return vol_per_5
# Function to get the year component from the date
def get_year(df):
    year_comp = pd.Series()
    for idx, row in df.iterrows():
        year_comp.loc[idx] = int(row['Date'].year)
    return year_comp
# Assigning the newly created indicators to the dataframe
sphist_close['avg_per_5'] = five_day_avg(sphist_close)
sphist_close['std_per_30'] = thirty_day_std(sphist_close)
sphist_close['avg_per_365'] = year_avg(sphist_close)
sphist_close['vol_per_5'] = five_day_vol(sphist_close)
sphist_close['year_comp'] = get_year(sphist_close)

# Dropping data that contains null values
sphist_close = sphist_close[sphist_close['Date'] >= '1951-01-01']
sphist_close = sphist_close.dropna(axis=0)

# Creating Train and Test datasets
train = sphist_close[sphist_close['Date'] < '2013-01-01']
test = sphist_close[sphist_close['Date'] >= '2013-01-01']

train_X = train.drop(['Date','Close','index'], axis=1)
train_y = train['Close']
test_X = test.drop(['Date','Close','index'], axis=1)
test_y = test['Close']

# Initiating Linear Regression model
lr = LinearRegression()
# Fitting the model
lr.fit(train_X, train_y)
# Making predictions 
predictions = lr.predict(test_X)
# Calculating the error
error = mean_absolute_error(test_y, predictions)

print(error)