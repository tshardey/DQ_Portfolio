
# coding: utf-8

# # Analyzing Thanksgiving Dinner
# 
# ## Importing Data
# 
# The dataset is stored in the thanksgiving.csv file. It contains 1058 responses to an online survey about what Americans eat for Thanksgiving dinner. Each survey respondent was asked questions about what they typically eat for Thanksgiving, along with some demographic questions, like their gender, income, and location. 

# In[23]:


import pandas as pd
# Importing the Thanksgiving data from a CSV file
data = pd.read_csv("thanksgiving.csv", encoding="Latin-1")
# Previewing the data to make sure it was imported correctly 
print(data.head(2))

# Capturing the columns
columns = data.columns
# Previewing column data to make sure it captured correctly 
print(columns[:5])


# ## Those who celebrate Thanksgiving
# 
# Because we want to understand what people ate for Thanksgiving, we'll remove any responses from people who don't celebrate it. The column Do you celebrate Thanksgiving? contains this information. We only want to keep data for people who answered Yes to this questions.

# In[24]:


# Shortcut for column name 
celebrate_text = "Do you celebrate Thanksgiving?"
# Looking at how many times each value occurs in the column
celebrate = data[celebrate_text].value_counts()
print("\nThe number of people who do/don't celebrate Thanksgiving: ")
print(celebrate)


# In[25]:


# Filtering data to only include individuals who celebrate Thanksgiving
data = data[data[celebrate_text] == "Yes"]


# ## Thanksgiving Main Dishes
# 
# Exploring what main dishes people tend to eat during Thanksgiving dinner

# In[26]:


main_dish_text = "What is typically the main dish at your Thanksgiving dinner?"
gravy_text = "Do you typically have gravy?"

# Categorize all of the values for Thanksgiving's main dishes
main_dish_values = data[main_dish_text].value_counts()
print("\nCategorical values for potential main dishes on Thanksgiving: ")
print(main_dish_values)


# In[27]:


# Creating shortcut text
gravy_text = "Do you typically have gravy?"
# Filtering the dataset to only include a main dish of tofurkey
tofurkey = data[data[main_dish_text] == "Tofurkey"]
# Looking at the column to determine if they have gravy with their tofurkey
tofurkey_gravy = tofurkey[gravy_text]
print("\nResponses of people who might have gravy with their tofurkey:")
print(tofurkey_gravy)


# ## Thanksgiving Dessert
# 
# Let's explore the dessert dishes. Specifically, we'll look at how many people eat Apple, Pecan, or Pumpkin pie during Thanksgiving dinner.
# 
# We can find out how many people eat one of these three pies for Thanksgiving dinner by figuring out for how many people all three columns are null.

# In[28]:


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


# ## Ages
# 
# Let's analyze the Age column in more depth. In order to analyze the Age column, we'll first need to convert it to numeric values. This will make it simple to figure out things like the average age of survey respondents.
# 
# We can do this by splitting each value on the space character (), then taking the first item in the resulting list. We'll also have to replace the + character to account for 60+, which follows a different format than the rest.
# 
# Or this can be done using regular expressions.  

# In[29]:


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
        


# In[30]:


# Applying the function to each row of the "Age" column
int_age = data["Age"].apply(age_extract)
# Adding a new column with the integer value approximations to the dataframe
data["int_Age"] = int_age
# Verifying work 
print("\nValue counts by age approximation:")
print(data["int_Age"].value_counts())


# ## Average Household Income
# The How much total combined money did all members of your HOUSEHOLD earn last year? column is very similar to the Age column. It contains categories, but can be converted to numerical values.
# 
# We can convert these values to numeric by again splitting on the space character (). We'll then have to account for the string Prefer. Finally, we'll be able to replace the dollar sign character $ and the comma ,, and return the result.
# 
# Or this can be done using regular expressions. 

# In[31]:


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


# In[32]:


# Shortcut text
income_text = "How much total combined money did all members of your HOUSEHOLD earn last year?"
# Applying income extraction to all rows in the income column
int_income = data[income_text].apply(income_extract)
# Adding integer income value approximations to the dataframe
data["int_Income"] = int_income
# Checking work
print("\nIncome approximation counts:")
print(data["int_Income"].value_counts())


# ## Issues with approximation
# 
# The method for converting ages and income into integer values when a range is given has its flaws.  The data could be skewed to one side of the age range or the income range, which could inter deliver very different results.  Alternatives would be to make a min and a max column, or two average the two values at the end of the bracket.  While neither of those methods are perfect, the do try to make the most out of the data that was given.  
# 
# The ages were almost equally distributed with the exception of the lowest age bracket, represented as "18."  However there was a clear skew of data to the lower incomes in regards to celebrating income.  My guess is this has more to do with there being more low income families who took the survey, or in general in the U.S., instead of it indicating that lower income families are more likely to celebrate Thanksgiving.  

# ## Travel
# 
# We can now see how the distance someone travels for Thanksgiving dinner relates to their income level. It's safe to hypothesize that people earning less money could be younger, and would travel to their parent's houses for Thanksgiving. People earning more are more likely to have Thanksgiving at their house as a result.
# 
# We can test this by filtering data based on int_income, and seeing what the values in the How far will you travel for Thanksgiving? column are.

# In[33]:


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


# ## Travel Conclusions
# 
# I altered the data to look at a cut off point of \$100k, because I felt that was a more accurate representation than $150 and it was in the middle of the income ranges.
# 
# The porportions of people willing to travel for thanksgiving seem roughly similar.  While travel is influenced by financial situation, there are many who prefer to stay home for Thanksgiving.  

# ## Thanksgiving with Friends 
# There are two columns which directly pertain to friendship, Have you ever tried to meet up with hometown friends on Thanksgiving night?, and Have you ever attended a "Friendsgiving?". In the US, a "Friendsgiving" is when instead of traveling home for the holiday, you celebrate it with friends who live in your area. Both questions seem skewed towards younger people. In order to see the average ages of people who have done both, we can use a pivot table.
# 

# In[34]:


# Shortcut text
hometown_friends_text = "Have you ever tried to meet up with hometown friends on Thanksgiving night?"
friendsgiving_text = "Have you ever attended a \"Friendsgiving?\""
print("\nThanksgiving with Friends by age:")
# A pivot table with friends data based on age
print(data.pivot_table(index = hometown_friends_text, columns = friendsgiving_text, values = "int_Age" ))


# In[35]:


print("\nThanksgiving with Friends by income:")
# A pivot table with friends data based on income
print(data.pivot_table(index = hometown_friends_text, columns = friendsgiving_text, values = "int_Income" ))


# ## Thanksgiving with Friends Conclusion
# 
# Those who celebrate "friendsgiving" were younger than those who didn't.  Individuals who tried to meet up with hometown friends and celebrated friendsgiving had a lower average age than those who didn't do either.  Similar trends can be seen when looking at average income.  This makes sense as younger individuals, especially those right out of school, are expected to have a lower average income.  

# In[36]:


print(data.columns)


# ## Popular Meals
# 
# Looking at the most popular side dishes and desserts.

# In[49]:


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


# In[53]:


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


# In[55]:


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


# ## Most Popular Conclusions:
# 
# It was not that surprising that the most popular side dish was mashed potatoes. It is a Thanksgiving classic.  While pie is typically portrayed as a popular dessert for Thanksgiving, it was still surprising that more people had no extra desserts.  

# ## Shopping Habits and Income

# In[59]:


# Looking at the average income for those who work Black Friday and work in retail
data.pivot_table(index = 'Do you work in retail?', columns = 'Will you employer make you work on Black Friday?' , values = 'int_Income' )


# In[60]:


# Looking at the average income for those who work Black Friday and work in retail
data.pivot_table(index = 'Will you shop any Black Friday sales on Thanksgiving Day?', columns = 'Will you employer make you work on Black Friday?' , values = 'int_Income' )


# In[62]:


# Looking at the average income for those who will shop black Friday and what geographical region they live in
data.pivot_table(index = 'Will you shop any Black Friday sales on Thanksgiving Day?', columns = 'US Region' , values = 'int_Income' )


# ## Shopping Habits Conclusions
# 
# The average income for those working vs not working on black friday was similar.  Those who were not shopping on black friday had over 2x the average income than those who were.  The income of potential shoppers of black Friday sales is pretty even in the East Central regions, West North Central and the Mid Atlantic, but skews towards higher income individuals not shopping in Mountain, New England, Pacific, South Atlanic, West South Central. 

# ## Religion by Region
# 

# In[64]:


# Shortcut Text
pray_text = "Do you typically pray before or after the Thanksgiving meal?"
# Subsetting the data to those who pray
religion_data = data[data[pray_text] == "Yes"]
# Looking at the counts for the regions where individuals pray at dinner
religion_data["US Region"].value_counts()


# ## Religion Conclusions
# 
# Prayer was more common in the South, and in the East and became less common as the geographical regions hit the central United States.  
