

```python
f = open("US_births_1994-2003_CDC_NCHS.csv")
births = f.read().split("\n")

```


```python
#function to read and parse a csv file 
def read_csv(fileName):
    f = open(fileName)
    data = f.read().split("\n")
    string_list = data[1:len(data)]
    final_list = []
    string_fields = []
    for string in string_list:
        int_fields = [] 
        string_fields = string.split(",")
        for field in string_fields:
            int_fields.append(int(field))
        final_list.append(int_fields)
    return final_list

cdc_list = read_csv("US_births_1994-2003_CDC_NCHS.csv")
```


```python
# Determing the total births per month from a list of lists
def month_births(listOfLists):
    births_per_month = {}
    for birth in listOfLists:
        if birth[1] in births_per_month:
            births_per_month[birth[1]] = births_per_month[birth[1]] + birth[4]
        else:
            births_per_month[birth[1]] = birth[4]
    return births_per_month

cdc_month_births = month_births(cdc_list)
print("Dictinary of births by month:")
print(cdc_month_births)
```

    Dictinary of births by month:
    {1: 3232517, 2: 3018140, 3: 3322069, 4: 3185314, 5: 3350907, 6: 3296530, 7: 3498783, 8: 3525858, 9: 3439698, 10: 3378814, 11: 3171647, 12: 3301860}



```python
# Determing the total births per day of the week from a list of lists
def dow_births(listOfLists):
    day_of_week = {}
    for birth in listOfLists:
        if birth[3] in day_of_week:
            day_of_week[birth[3]] = day_of_week[birth[3]] + birth[4]
        else:
            day_of_week[birth[3]] = birth[4]
    return day_of_week

cdc_day_births = dow_births(cdc_list)
print("\n Dictionary of births by day of the week:")
print(cdc_day_births)
```

    
     Dictionary of births by day of the week:
    {1: 5789166, 2: 6446196, 3: 6322855, 4: 6288429, 5: 6233657, 6: 4562111, 7: 4079723}



```python
# Calculate the total number of births by set value
def calc_counts(listOfLists, column):
    column_dict = {}
    for birth in listOfLists:
        if birth[column] in column_dict:
            column_dict[birth[column]] = column_dict[birth[column]] + birth[4]
        else:
            column_dict[birth[column]] = birth[4]
    return column_dict

cdc_year_births = calc_counts(cdc_list, 0)
cdc_month_births = calc_counts(cdc_list, 1)
cdc_dom_births = calc_counts(cdc_list, 2)
cdc_ydow_births = calc_counts(cdc_list, 3)
print("\nDictionary of births by year (1994-2003):")
print(cdc_year_births)
```

    
    Dictionary of births by year (1994-2003):
    {2000: 4058814, 2001: 4025933, 2002: 4021726, 2003: 4089950, 1994: 3952767, 1995: 3899589, 1996: 3891494, 1997: 3880894, 1998: 3941553, 1999: 3959417}



```python
# Find the min of a dictionary 
def min_dict(dictionary):
    index = 100000000
    for sets in dictionary:
        if dictionary[sets] < index:
            index = dictionary[sets]
            key = sets
    return key

print("\nMinimum year in the CDC Dictionary - " + str(min_dict(cdc_year_births)))

```

    
    Minimum year in the CDC Dictionary - 1997



```python
# Find the max of a dictionary 
def max_dict(dictionary):
    index = 0
    for sets in dictionary:
        if dictionary[sets] > index:
            index = dictionary[sets]
            key = sets
    return key

print("\nMaximum year in the CDC Dictionary - " + str(max_dict(cdc_year_births)))

```

    
    Maximum year in the CDC Dictionary - 2003



```python
# Calculating the difference per year from a list of lists based on the subgroup of a column
def diff_dict(listOflists, year, variable, variableName):
    ofInterest = []
    for lists in listOflists:
        if lists[0] == year and lists[variable] == variableName:
            ofInterest.append(lists)
    return sum(ofInterest[4])


print("\nDifference between births in 2000 in August and October: " + str(diff_dict(cdc_list, 2000, 1, 10) - diff_dict(cdc_list, 2000, 1, 8)))
```

    
    Difference between births in 2000 in August and October: 3707



```python
SSA_list = read_csv("US_births_2000-2014_SSA.csv")
```


```python
# Compiling one list (gives preference to the first list)
def compiled_list(listOne, listTwo):
    new_list = []
    for item in listOne:
        if item not in new_list:
            new_list.append(item)
    for item in listTwo:
        if item not in new_list:
            new_list.append(item)
    return new_list

total_list = compiled_list(cdc_list, SSA_list)
```


```python
# Checking the differences between the two lists and the combined list
print("\nCDC List")
print(len(cdc_list))
print("\nSSA List")
print(len(SSA_list))
print("\nTotal List")
print(len(total_list))
```

    
    CDC List
    3652
    
    SSA List
    5479
    
    Total List
    9131


For the combined list function, preference was given to the data in the CDC list, this could easily be switched.  Another way to handle the data would have been to take an average of the two values and 
