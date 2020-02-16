## 3. Reading in to Pandas ##

import pandas as pd

loans_2007 = pd.read_csv("loans_2007.csv")
print(loans_2007.head(1))
print(loans_2007.shape[1])

## 5. First group of columns ##

columns_to_drop = ['id', 'member_id', 'funded_amnt', 'funded_amnt_inv', 'grade', 'sub_grade', 'emp_title', 'issue_d']

loans_2007.drop(columns_to_drop, axis=1, inplace=True)

## 7. Second group of features ##

columns_to_drop2 = ['zip_code', 'out_prncp', 'out_prncp_inv', 'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp']
loans_2007 = loans_2007.drop(columns_to_drop2, axis=1)

## 9. Third group of features ##

columns_to_drop3 = ['total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee', 'last_pymnt_amnt', 'last_pymnt_d']

loans_2007.drop(columns_to_drop3, axis=1, inplace=True)

## 10. Target column ##

print(loans_2007['loan_status'].value_counts())

## 12. Binary classification ##

fully_paid = loans_2007['loan_status'] == 'Fully Paid'
charged_off = loans_2007['loan_status'] == 'Charged Off'

loans_2007 = loans_2007[fully_paid |charged_off]

mapping_dict = {
    'loan_status': {
        'Fully Paid': 1,
        'Charged Off': 0
    }
}
    
loans_2007 = loans_2007.replace(mapping_dict)                                                     

## 13. Removing single value columns ##

drop_columns = []

for col in loans_2007.columns:
    non_null = loans_2007[col].dropna()
    unique_non_null = non_null.unique()
    num_true_unique = len(unique_non_null)
    if num_true_unique == 1:
        drop_columns.append(col)
        
loans_2007.drop(drop_columns, axis=1, inplace=True)

print(drop_columns)