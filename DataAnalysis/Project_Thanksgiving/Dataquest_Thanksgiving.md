
# Analyzing Thanksgiving Dinner

## Importing Data

The dataset is stored in the thanksgiving.csv file. It contains 1058 responses to an online survey about what Americans eat for Thanksgiving dinner. Each survey respondent was asked questions about what they typically eat for Thanksgiving, along with some demographic questions, like their gender, income, and location. 


```python
import pandas as pd
# Importing the Thanksgiving data from a CSV file
data = pd.read_csv("thanksgiving.csv", encoding="Latin-1")
# Previewing the data to make sure it was imported correctly 
print(data.head(2))

# Capturing the columns
columns = data.columns
# Previewing column data to make sure it captured correctly 
print(columns[:5])
```

       RespondentID Do you celebrate Thanksgiving?  \
    0    4337954960                            Yes   
    1    4337951949                            Yes   
    
      What is typically the main dish at your Thanksgiving dinner?  \
    0                                             Turkey             
    1                                             Turkey             
    
      What is typically the main dish at your Thanksgiving dinner? - Other (please specify)  \
    0                                                NaN                                      
    1                                                NaN                                      
    
      How is the main dish typically cooked?  \
    0                                  Baked   
    1                                  Baked   
    
      How is the main dish typically cooked? - Other (please specify)  \
    0                                                NaN                
    1                                                NaN                
    
      What kind of stuffing/dressing do you typically have?  \
    0                                        Bread-based      
    1                                        Bread-based      
    
      What kind of stuffing/dressing do you typically have? - Other (please specify)  \
    0                                                NaN                               
    1                                                NaN                               
    
      What type of cranberry saucedo you typically have?  \
    0                                               None   
    1                             Other (please specify)   
    
      What type of cranberry saucedo you typically have? - Other (please specify)  \
    0                                                NaN                            
    1                    Homemade cranberry gelatin ring                            
    
              ...          \
    0         ...           
    1         ...           
    
      Have you ever tried to meet up with hometown friends on Thanksgiving night?  \
    0                                                Yes                            
    1                                                 No                            
    
      Have you ever attended a "Friendsgiving?"  \
    0                                        No   
    1                                        No   
    
      Will you shop any Black Friday sales on Thanksgiving Day?  \
    0                                                 No          
    1                                                Yes          
    
      Do you work in retail? Will you employer make you work on Black Friday?  \
    0                     No                                              NaN   
    1                     No                                              NaN   
    
      How would you describe where you live?      Age What is your gender?  \
    0                               Suburban  18 - 29                 Male   
    1                                  Rural  18 - 29               Female   
    
      How much total combined money did all members of your HOUSEHOLD earn last year?  \
    0                                 $75,000 to $99,999                                
    1                                 $50,000 to $74,999                                
    
                US Region  
    0     Middle Atlantic  
    1  East South Central  
    
    [2 rows x 65 columns]
    Index(['RespondentID', 'Do you celebrate Thanksgiving?',
           'What is typically the main dish at your Thanksgiving dinner?',
           'What is typically the main dish at your Thanksgiving dinner? - Other (please specify)',
           'How is the main dish typically cooked?'],
          dtype='object')


## Those who celebrate Thanksgiving

Because we want to understand what people ate for Thanksgiving, we'll remove any responses from people who don't celebrate it. The column Do you celebrate Thanksgiving? contains this information. We only want to keep data for people who answered Yes to this questions.


```python
# Shortcut for column name 
celebrate_text = "Do you celebrate Thanksgiving?"
# Looking at how many times each value occurs in the column
celebrate = data[celebrate_text].value_counts()
print("\nThe number of people who do/don't celebrate Thanksgiving: ")
print(celebrate)
```

    
    The number of people who do/don't celebrate Thanksgiving: 
    Yes    980
    No      78
    Name: Do you celebrate Thanksgiving?, dtype: int64



```python
# Filtering data to only include individuals who celebrate Thanksgiving
data = data[data[celebrate_text] == "Yes"]

```

## Thanksgiving Main Dishes

Exploring what main dishes people tend to eat during Thanksgiving dinner


```python
main_dish_text = "What is typically the main dish at your Thanksgiving dinner?"
gravy_text = "Do you typically have gravy?"

# Categorize all of the values for Thanksgiving's main dishes
main_dish_values = data[main_dish_text].value_counts()
print("\nCategorical values for potential main dishes on Thanksgiving: ")
print(main_dish_values)
```

    
    Categorical values for potential main dishes on Thanksgiving: 
    Turkey                    859
    Other (please specify)     35
    Ham/Pork                   29
    Tofurkey                   20
    Chicken                    12
    Roast beef                 11
    I don't know                5
    Turducken                   3
    Name: What is typically the main dish at your Thanksgiving dinner?, dtype: int64



```python
# Creating shortcut text
gravy_text = "Do you typically have gravy?"
# Filtering the dataset to only include a main dish of tofurkey
tofurkey = data[data[main_dish_text] == "Tofurkey"]
# Looking at the column to determine if they have gravy with their tofurkey
tofurkey_gravy = tofurkey[gravy_text]
print("\nResponses of people who might have gravy with their tofurkey:")
print(tofurkey_gravy)
```

    
    Responses of people who might have gravy with their tofurkey:
    4      Yes
    33     Yes
    69      No
    72      No
    77     Yes
    145    Yes
    175    Yes
    218     No
    243    Yes
    275     No
    393    Yes
    399    Yes
    571    Yes
    594    Yes
    628     No
    774     No
    820     No
    837    Yes
    860     No
    953    Yes
    Name: Do you typically have gravy?, dtype: object


## Thanksgiving Dessert

Let's explore the dessert dishes. Specifically, we'll look at how many people eat Apple, Pecan, or Pumpkin pie during Thanksgiving dinner.

We can find out how many people eat one of these three pies for Thanksgiving dinner by figuring out for how many people all three columns are null.


```python
# Shortcut text
apple_text = "Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple"
pumpkin_text = "Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin"
pecan_text = "Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan"

# Checking whether each pie is typically eaten
apple_isnull = data[apple_text].isnull()
pumpkin_isnull = data[pumpkin_text].isnull()
pecan_isnull = data[pecan_text].isnull()

# Looking at whether all pies or no pies were eaten  
no_pies = apple_isnull & pumpkin_isnull & pecan_isnull
print("\nI eat a lot of different pie: ")
print(no_pies.value_counts())
```

    
    I eat a lot of different pie: 
    False    876
    True     104
    dtype: int64


## Ages

Let's analyze the Age column in more depth. In order to analyze the Age column, we'll first need to convert it to numeric values. This will make it simple to figure out things like the average age of survey respondents.

We can do this by splitting each value on the space character (), then taking the first item in the resulting list. We'll also have to replace the + character to account for 60+, which follows a different format than the rest.

Or this can be done using regular expressions.  


```python
import re

# Defining a function to extract the first age from the brackets in the "Age" column
def age_extract(string):
    # regular expression for any potential age value less than 3-digits
    regex_age = "^[0-9]{2}"
    # Checking whether the string is a null value
    if pd.isnull(string):
        return None
    else:
        age_list = re.findall(regex_age, string)
        return int(age_list[0])
        
```


```python
# Applying the function to each row of the "Age" column
int_age = data["Age"].apply(age_extract)
# Adding a new column with the integer value approximations to the dataframe
data["int_Age"] = int_age
# Verifying work 
print("\nValue counts by age approximation:")
print(data["int_Age"].value_counts())
```

    
    Value counts by age approximation:
    45.0    269
    60.0    258
    30.0    235
    18.0    185
    Name: int_Age, dtype: int64


## Average Household Income
The How much total combined money did all members of your HOUSEHOLD earn last year? column is very similar to the Age column. It contains categories, but can be converted to numerical values.

We can convert these values to numeric by again splitting on the space character (). We'll then have to account for the string Prefer. Finally, we'll be able to replace the dollar sign character $ and the comma ,, and return the result.

Or this can be done using regular expressions. 


```python
# Defining a function to extract the lower bound of the income bracked=t
def income_extract(string):
    regex_income = "^\$[0-9]{0,3},?[0-9]{0,3}"
    if pd.isnull(string):
        return None
    else:
        income_list = re.findall(regex_income, string)
        try:
            income = income_list[0]
            strip_income = re.sub("," , "", income[1:])
            return int(strip_income)
        except:
            return None
```


```python
# Shortcut text
income_text = "How much total combined money did all members of your HOUSEHOLD earn last year?"
# Applying income extraction to all rows in the income column
int_income = data[income_text].apply(income_extract)
# Adding integer income value approximations to the dataframe
data["int_Income"] = int_income
# Checking work
print("\nIncome approximation counts:")
print(data["int_Income"].value_counts())

```

    
    Income approximation counts:
    25000.0     166
    75000.0     127
    50000.0     127
    100000.0    109
    200000.0     76
    10000.0      60
    0.0          52
    125000.0     48
    150000.0     38
    175000.0     26
    Name: int_Income, dtype: int64


## Issues with approximation

The method for converting ages and income into integer values when a range is given has its flaws.  The data could be skewed to one side of the age range or the income range, which could inter deliver very different results.  Alternatives would be to make a min and a max column, or two average the two values at the end of the bracket.  While neither of those methods are perfect, the do try to make the most out of the data that was given.  

The ages were almost equally distributed with the exception of the lowest age bracket, represented as "18."  However there was a clear skew of data to the lower incomes in regards to celebrating income.  My guess is this has more to do with there being more low income families who took the survey, or in general in the U.S., instead of it indicating that lower income families are more likely to celebrate Thanksgiving.  

## Travel

We can now see how the distance someone travels for Thanksgiving dinner relates to their income level. It's safe to hypothesize that people earning less money could be younger, and would travel to their parent's houses for Thanksgiving. People earning more are more likely to have Thanksgiving at their house as a result.

We can test this by filtering data based on int_income, and seeing what the values in the How far will you travel for Thanksgiving? column are.


```python
# Shortcut text
travel_text = "How far will you travel for Thanksgiving?"
# Dividing the data to look at only incomes less that $100k
lower_income = data[data["int_Income"] < 100000]
print("\nTravel for those who earn less than $100k:")
# Looking at how many people travel for Thanksgiving based on income.
print(lower_income[travel_text].value_counts())

# Dividing the data to look at income values higher than or equal to $100k.
higher_income = data[data["int_Income"] >= 100000]
print("\nTravel for those who earn more than $100k:")
# Looking at how many people travel for Thanksgiving based on income.
print(higher_income[travel_text].value_counts())

```

    
    Travel for those who earn less than $100k:
    Thanksgiving is happening at my home--I won't travel at all                         205
    Thanksgiving is local--it will take place in the town I live in                     163
    Thanksgiving is out of town but not too far--it's a drive of a few hours or less    126
    Thanksgiving is out of town and far away--I have to drive several hours or fly       38
    Name: How far will you travel for Thanksgiving?, dtype: int64
    
    Travel for those who earn more than $100k:
    Thanksgiving is happening at my home--I won't travel at all                         142
    Thanksgiving is local--it will take place in the town I live in                      74
    Thanksgiving is out of town but not too far--it's a drive of a few hours or less     49
    Thanksgiving is out of town and far away--I have to drive several hours or fly       32
    Name: How far will you travel for Thanksgiving?, dtype: int64


## Travel Conclusions

I altered the data to look at a cut off point of \$100k, because I felt that was a more accurate representation than $150 and it was in the middle of the income ranges.

The porportions of people willing to travel for thanksgiving seem roughly similar.  While travel is influenced by financial situation, there are many who prefer to stay home for Thanksgiving.  

## Thanksgiving with Friends 
There are two columns which directly pertain to friendship, Have you ever tried to meet up with hometown friends on Thanksgiving night?, and Have you ever attended a "Friendsgiving?". In the US, a "Friendsgiving" is when instead of traveling home for the holiday, you celebrate it with friends who live in your area. Both questions seem skewed towards younger people. In order to see the average ages of people who have done both, we can use a pivot table.



```python
# Shortcut text
hometown_friends_text = "Have you ever tried to meet up with hometown friends on Thanksgiving night?"
friendsgiving_text = "Have you ever attended a \"Friendsgiving?\""
print("\nThanksgiving with Friends by age:")
# A pivot table with friends data based on age
print(data.pivot_table(index = hometown_friends_text, columns = friendsgiving_text, values = "int_Age" ))
```

    
    Thanksgiving with Friends by age:
    Have you ever attended a "Friendsgiving?"                  No        Yes
    Have you ever tried to meet up with hometown fr...                      
    No                                                  42.283702  37.010526
    Yes                                                 41.475410  33.976744



```python
print("\nThanksgiving with Friends by income:")
# A pivot table with friends data based on income
print(data.pivot_table(index = hometown_friends_text, columns = friendsgiving_text, values = "int_Income" ))
```

    
    Thanksgiving with Friends by income:
    Have you ever attended a "Friendsgiving?"                     No           Yes
    Have you ever tried to meet up with hometown fr...                            
    No                                                  78914.549654  72894.736842
    Yes                                                 78750.000000  66019.736842


## Thanksgiving with Friends Conclusion

Those who celebrate "friendsgiving" were younger than those who didn't.  Individuals who tried to meet up with hometown friends and celebrated friendsgiving had a lower average age than those who didn't do either.  Similar trends can be seen when looking at average income.  This makes sense as younger individuals, especially those right out of school, are expected to have a lower average income.  


```python
print(data.columns)
```

    Index(['RespondentID', 'Do you celebrate Thanksgiving?',
           'What is typically the main dish at your Thanksgiving dinner?',
           'What is typically the main dish at your Thanksgiving dinner? - Other (please specify)',
           'How is the main dish typically cooked?',
           'How is the main dish typically cooked? - Other (please specify)',
           'What kind of stuffing/dressing do you typically have?',
           'What kind of stuffing/dressing do you typically have? - Other (please specify)',
           'What type of cranberry saucedo you typically have?',
           'What type of cranberry saucedo you typically have? - Other (please specify)',
           'Do you typically have gravy?',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Brussel sprouts',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Carrots',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Cauliflower',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Corn',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Cornbread',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Fruit salad',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Green beans/green bean casserole',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Macaroni and cheese',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Mashed potatoes',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Rolls/biscuits',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Squash',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Vegetable salad',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Yams/sweet potato casserole',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Other (please specify)',
           'Which of these side dishes aretypically served at your Thanksgiving dinner? Please select all that apply. - Other (please specify).1',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Buttermilk',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Cherry',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Chocolate',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Coconut cream',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Key lime',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Peach',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Sweet Potato',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - None',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Other (please specify)',
           'Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Other (please specify).1',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Apple cobbler',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Blondies',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Brownies',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Carrot cake',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Cheesecake',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Cookies',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Fudge',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Ice cream',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Peach cobbler',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - None',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Other (please specify)',
           'Which of these desserts do you typically have at Thanksgiving dinner? Please select all that apply.   - Other (please specify).1',
           'Do you typically pray before or after the Thanksgiving meal?',
           'How far will you travel for Thanksgiving?',
           'Will you watch any of the following programs on Thanksgiving? Please select all that apply. - Macy's Parade',
           'What's the age cutoff at your "kids' table" at Thanksgiving?',
           'Have you ever tried to meet up with hometown friends on Thanksgiving night?',
           'Have you ever attended a "Friendsgiving?"',
           'Will you shop any Black Friday sales on Thanksgiving Day?',
           'Do you work in retail?',
           'Will you employer make you work on Black Friday?',
           'How would you describe where you live?', 'Age', 'What is your gender?',
           'How much total combined money did all members of your HOUSEHOLD earn last year?',
           'US Region', 'int_Age', 'int_Income'],
          dtype='object')


## Popular Meals

Looking at the most popular side dishes and desserts.


```python
# The column names are very bulky so a function was created to strip off the name of the dish from the column 
# name and discard the rest.  
def strip_col_name(string):
    # Finds any value occuring after a "-"
    regex_name = " - .{0,35}"
    # Searches string
    names = re.findall(regex_name, string)
    # Checks to see if a dash is in the string, if it is, it returns the string unchanged
    if "-" not in string:
        return string
    # Tries to subset the string, if it can't it will return the string unchanged
    else:
        try: 
            name = names[0]
            return name[3:]
        except:
            return string

# Applying the function to strip the column names on a series containing the column names
new_column_names = pd.Series(columns).apply(strip_col_name)

# Creating an empty dictionary
dictionary_names = {}

# Looping through columns to assign the old column names to the new column names
for i in range(1,len(columns)):
    dictionary_names[columns[i]] = new_column_names[i]

# Renaming the columns of data
data.rename(index=str, columns=dictionary_names, inplace=True)
```


```python
# Creating a dataframe that only looks at the side dish options
side_dish = data.iloc[:, 11:24]
# Checking which values of the column are null and substracting that from the length of the dataframe to get the
# number of non-null values.  
pop_side_dishes = len(side_dish) - pd.isnull(side_dish).sum()
# Finding the index of the minimum value 
min_side_dish = pop_side_dishes[pop_side_dishes == pop_side_dishes.min()].index
print("Least popular side dish: " + min_side_dish)
# Finding the index of the maximum value
max_side_dish = pop_side_dishes[pop_side_dishes == pop_side_dishes.max()].index
print("Most popular side dish: " + max_side_dish)
```

    Index(['Least popular side dish: Cauliflower'], dtype='object')
    Index(['Most popular side dish: Mashed potatoes'], dtype='object')



```python
# Creating a dataframe that only looks at the dessert options outside of pie
dessert = data.iloc[:, 39:51]
# Checking which values of the column are null and substracting that from the length of the dataframe to get the
# number of non-null values.  
pop_dessert = len(dessert) - pd.isnull(dessert).sum()
# Finding the index of the minimum value 
min_dessert = pop_dessert[pop_dessert == pop_dessert.min()].index
print("Least popular dessert: " + min_dessert)
# Finding the index of the maximum value
max_dessert = pop_dessert[pop_dessert == pop_dessert.max()].index
print("Most popular dessert: " + max_dessert)
```

    Index(['Least popular dessert: Blondies'], dtype='object')
    Index(['Most popular dessert: None'], dtype='object')


## Most Popular Conclusions:

It was not that surprising that the most popular side dish was mashed potatoes. It is a Thanksgiving classic.  While pie is typically portrayed as a popular dessert for Thanksgiving, it was still surprising that more people had no extra desserts.  

## Shopping Habits and Income


```python
# Looking at the average income for those who work Black Friday and work in retail
data.pivot_table(index = 'Do you work in retail?', columns = 'Will you employer make you work on Black Friday?' , values = 'int_Income' )
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Will you employer make you work on Black Friday?</th>
      <th>Doesn't apply</th>
      <th>No</th>
      <th>Yes</th>
    </tr>
    <tr>
      <th>Do you work in retail?</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Yes</th>
      <td>57000.0</td>
      <td>51944.444444</td>
      <td>56666.666667</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Looking at the average income for those who work Black Friday and work in retail
data.pivot_table(index = 'Will you shop any Black Friday sales on Thanksgiving Day?', columns = 'Will you employer make you work on Black Friday?' , values = 'int_Income' )
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Will you employer make you work on Black Friday?</th>
      <th>Doesn't apply</th>
      <th>No</th>
      <th>Yes</th>
    </tr>
    <tr>
      <th>Will you shop any Black Friday sales on Thanksgiving Day?</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>No</th>
      <td>37500.0</td>
      <td>75000.000000</td>
      <td>75909.090909</td>
    </tr>
    <tr>
      <th>Yes</th>
      <td>70000.0</td>
      <td>28888.888889</td>
      <td>31764.705882</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Looking at the average income for those who will shop black Friday and what geographical region they live in
data.pivot_table(index = 'Will you shop any Black Friday sales on Thanksgiving Day?', columns = 'US Region' , values = 'int_Income' )
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>US Region</th>
      <th>East North Central</th>
      <th>East South Central</th>
      <th>Middle Atlantic</th>
      <th>Mountain</th>
      <th>New England</th>
      <th>Pacific</th>
      <th>South Atlantic</th>
      <th>West North Central</th>
      <th>West South Central</th>
    </tr>
    <tr>
      <th>Will you shop any Black Friday sales on Thanksgiving Day?</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>No</th>
      <td>74207.920792</td>
      <td>64868.421053</td>
      <td>91050.0</td>
      <td>95000.000000</td>
      <td>94868.421053</td>
      <td>78453.608247</td>
      <td>79365.079365</td>
      <td>68936.170213</td>
      <td>89607.843137</td>
    </tr>
    <tr>
      <th>Yes</th>
      <td>74500.000000</td>
      <td>86333.333333</td>
      <td>87800.0</td>
      <td>54166.666667</td>
      <td>37500.000000</td>
      <td>47631.578947</td>
      <td>49100.000000</td>
      <td>59166.666667</td>
      <td>57400.000000</td>
    </tr>
  </tbody>
</table>
</div>



## Shopping Habits Conclusions

The average income for those working vs not working on black friday was similar.  Those who were not shopping on black friday had over 2x the average income than those who were.  The income of potential shoppers of black Friday sales is pretty even in the East Central regions, West North Central and the Mid Atlantic, but skews towards higher income individuals not shopping in Mountain, New England, Pacific, South Atlanic, West South Central. 

## Religion by Region



```python
# Shortcut Text
pray_text = "Do you typically pray before or after the Thanksgiving meal?"
# Subsetting the data to those who pray
religion_data = data[data[pray_text] == "Yes"]
# Looking at the counts for the regions where individuals pray at dinner
religion_data["US Region"].value_counts()
```




    South Atlantic        148
    East North Central     96
    Middle Atlantic        92
    Pacific                69
    West South Central     63
    East South Central     46
    West North Central     45
    New England            25
    Mountain               25
    Name: US Region, dtype: int64



## Religion Conclusions

Prayer was more common in the South, and in the East and became less common as the geographical regions hit the central United States.  
