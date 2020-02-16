## 1. Recap ##

import pandas as pd

loans = pd.read_csv('cleaned_loans_2007.csv')

print(loans.info())

## 3. Picking an error metric ##

import pandas as pd

filter_tn = (predictions == 0) & (loans["loan_status"] == 0)
tn = len(loans[filter_tn])
filter_tp = (predictions == 1) & (loans["loan_status"] == 1)
tp = len(loans[filter_tp])
filter_fn = (predictions == 0) & (loans["loan_status"] == 1)
fn = len(loans[filter_fn])
filter_fp = (predictions == 1) & (loans["loan_status"] == 0)
fp = len(loans[filter_fp])


## 5. Class imbalance ##

import pandas as pd
import numpy

# Predict that all loans will be paid off on time.
predictions = pd.Series(numpy.ones(loans.shape[0]))
# False positives.
fp_filter = (predictions == 1) & (loans["loan_status"] == 0)
fp = len(predictions[fp_filter])

# True positives.
tp_filter = (predictions == 1) & (loans["loan_status"] == 1)
tp = len(predictions[tp_filter])

# False negatives.
fn_filter = (predictions == 0) & (loans["loan_status"] == 1)
fn = len(predictions[fn_filter])

# True negatives
tn_filter = (predictions == 0) & (loans["loan_status"] == 0)
tn = len(predictions[tn_filter])

fpr = fp / (fp+tn)
tpr = tp / (tp+fn)

print(fpr, tpr)

## 6. Logistic Regression ##

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

features = loans.drop('loan_status', axis=1)
target = loans['loan_status']

lr.fit(features, target)
predictions = lr.predict(features)

## 7. Cross Validation ##

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
lr = LogisticRegression()
predictions = cross_val_predict(lr, features, target, cv=3)
predictions = pd.Series(predictions)

tp_filter = (target == 1) & (predictions==1)
tp = len(loans[tp_filter])
tn_filter = (target == 0) & (predictions==0)
tn = len(loans[tn_filter])
fp_filter = (target == 0) & (predictions==1)
fp = len(loans[fp_filter])
fn_filter = (target == 1) & (predictions==0)
fn = len(loans[fn_filter])

tpr = tp/(tp + fn)
fpr = fp/(fp+tn)

## 9. Penalizing the classifier ##

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
lr = LogisticRegression(class_weight = 'balanced')

predictions = cross_val_predict(lr, features, target)
predictions = pd.Series(predictions)

tp_filter = (target == 1) & (predictions==1)
tp = len(loans[tp_filter])
tn_filter = (target == 0) & (predictions==0)
tn = len(loans[tn_filter])
fp_filter = (target == 0) & (predictions==1)
fp = len(loans[fp_filter])
fn_filter = (target == 1) & (predictions==0)
fn = len(loans[fn_filter])

tpr = tp/(tp + fn)
fpr = fp/(fp+tn)

## 10. Manual penalties ##

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

penalty = {
    0: 10,
    1: 1
}
lr = LogisticRegression(class_weight=penalty)
predictions = cross_val_predict(lr, features, target)

tp_filter = (target == 1) & (predictions==1)
tp = len(loans[tp_filter])
tn_filter = (target == 0) & (predictions==0)
tn = len(loans[tn_filter])
fp_filter = (target == 0) & (predictions==1)
fp = len(loans[fp_filter])
fn_filter = (target == 1) & (predictions==0)
fn = len(loans[fn_filter])

tpr = tp/(tp + fn)
fpr = fp/(fp+tn)

## 11. Random forests ##

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_predict

penalty = {
    0: 10,
    1: 1
}
lr = RandomForestClassifier(random_state=1, class_weight='balanced')
predictions = cross_val_predict(lr, features, target)

tp_filter = (target == 1) & (predictions==1)
tp = len(loans[tp_filter])
tn_filter = (target == 0) & (predictions==0)
tn = len(loans[tn_filter])
fp_filter = (target == 0) & (predictions==1)
fp = len(loans[fp_filter])
fn_filter = (target == 1) & (predictions==0)
fn = len(loans[fn_filter])

tpr = tp/(tp + fn)
fpr = fp/(fp+tn)

print(tpr, fpr)