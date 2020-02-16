
# coding: utf-8

# # Winning Jeopardy
# 
# Jeopardy is a popular TV show in the US, that has been running for decades.  Participants answer questions from various categories in order to win money.   
# 
# The data used in this analysis is a subset of the following dataset:
# 
# https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/
# 
# Each row represents a single question on an episode of Jeopardy.  

# In[116]:


# Setting up the environment

import pandas as pd
from string import punctuation


# In[117]:


# Importing the data into a dataframe
jeopardy = pd.read_csv('jeopardy.csv')


# In[118]:


# Previewing the data
jeopardy.head()


# In[119]:


print("The column names are:\n{}".format(jeopardy.columns))


# In[120]:


# Renaming columns to remove the beginning space
column_names = jeopardy.columns
new_names = []
for name in column_names:
    if name.startswith(" "):
        new_names.append(name.replace(" ", "", 1))
    else:
        new_names.append(name)

print(new_names)


# In[121]:


# Reassigning the new names back to the columns
jeopardy.columns = new_names
print("The column names are:\n{}".format(jeopardy.columns))


# ## Normalizing the Q&A
# 
# The Series.apply() will be used, inconjunction with a fucntion created to:
# 1. Convert the string to lowercase
# 2. Remove all punctuation from the string

# In[122]:


# Creating a function to normalize the questions and answers
def clean_string(dirty_string):
    new_string = dirty_string.lower()
    table = str.maketrans({key: None for key in punctuation})
    new_string = new_string.translate(table)
    return new_string


# In[123]:


# Applying the clean_string function to the Question and Answer columns
jeopardy['clean_question'] = jeopardy['Question'].apply(clean_string)
jeopardy['clean_answer'] = jeopardy['Answer'].apply(clean_string)

jeopardy.head()


# ## Normalizing the Value column
# 
# The Series.apply() will be used, inconjunction with a fucntion created to:
# 1. Remove any punctuation in the string.
# 2. Convert the string to an integer.
# 3. If the conversion has an error, assign 0 instead.

# In[124]:


# Function to remove the punctuation and convert the value to an integer
def clean_value(dirty_value):
    try:
        table = str.maketrans({key: None for key in punctuation})
        new_value = int(dirty_value.translate(table))
    except:
        new_value = 0
    return new_value


# In[125]:


# Assigning the cleaned values to a new column
jeopardy['clean_value'] = jeopardy['Value'].apply(clean_value)
# Converting the Air Date to a datetime object
jeopardy['Air Date'] = pd.to_datetime(jeopardy['Air Date'])

print("The Air Date type is: {}".format(type(jeopardy['Air Date'][0])))
jeopardy.head(2)


# # What to study?
# In order to figure out whether to study past questions, study general knowledge, or not study it all, it would be helpful to figure out two things:
# 
# - How often the answer is deducible from the question.
# - How often new questions are repeats of older questions.
# 
# You can answer the second question by seeing how often complex words (> 6 characters) reoccur. You can answer the first question by seeing how many times words in the answer also occur in the question. We'll work on the first question now, and come back to the second.

# In[126]:


# Function to check whether answer occured in question
def answer_in_question(q_and_a):
    split_answer = q_and_a['clean_answer'].split(" ")
    split_question = q_and_a['clean_question'].split(" ")
    match_count = 0
    # removing the from answer
    if "the" in split_answer:
        split_answer.remove("the")
    if len(split_answer) == 0:
        return 0
    # checking to see if the word in the answer was in the question
    for answer in split_answer:
        if answer in split_question:
            match_count +=1
    # returning the number of words in the answer that appeared in the 
    # question and normalizing based on the length of the answer
    return match_count/len(split_answer)


# In[127]:


# Applying the answer_in_question function to each row of jeopardy
jeopardy['answer_in_question'] = jeopardy.apply(answer_in_question, axis =1)
jeopardy.head(2)


# In[128]:


print("The mean value for the answer appearing in the question is: {}".format(round(jeopardy['answer_in_question'].mean(), 4)))


# The resulting mean value indicates that depending on the answer to appear in the question is probably not a very sucessful method for winning Jeopardy.   

# In[129]:


# Looking at the number of repeat questions and topics
# An empty list to house the number of overlapping questions
questions_overlap = []
# An empty set to house the terms used
terms_used = set()

for index, question in jeopardy.iterrows():
    # splitting the cleaned question into individual words
    split_question = question['clean_question'].split(" ")
    # removing words from the list that are less than 6 characters
    split_question = [q for q in split_question if len(q) > 5]
    match_count = 0 
    # Checking to see if word is already in terms
    for word in split_question:
        if word in terms_used:
            match_count += 1
        # Adding word to terms
    for word in split_question:    
        terms_used.add(word)
    # normalizing based on the length of the question
    if len(split_question) > 0:
        match_count = match_count/len(split_question)
    questions_overlap.append(match_count)
# Adding the overlapping questions to jeopardy    
jeopardy['question_overlap'] = questions_overlap
jeopardy.head(2)


# In[130]:


# Looking at the mean value for overlapping questions
print("The mean for question_overlap is: {}".format(jeopardy['question_overlap'].mean()))


# Based on the mean value for the question_overlap column, looking at previous questions and subjects would be a better way to prepare for the show. 

# ## High vs. Low Value Questions
# 
# If you focus on high value questions the potential to earn more money is higher.  The values will be defined as:
# 
# - Low value -- Any row where Value is less than 800.
# - High value -- Any row where Value is greater than 800.
# 

# In[131]:


# Creating a function to assign a 0 or 1 based on the clean_value
def high_or_low(df_row):
    if df_row['clean_value'] > 800:
        value = 1
    else:
        value = 0
    return value


# In[132]:


# Applying the high_or_low function to jeopardy and assigning it to a new column
jeopardy['high_value'] = jeopardy.apply(high_or_low, axis=1)
jeopardy.head(2)


# In[133]:


# A function to determine how ofter the word appears and what the associated value was
def term_value(word):
    # Count holders
    low_count = 0 
    high_count = 0
    # looping through each row in jeopardy
    for index, row in jeopardy.iterrows():
        # spliting clean_question into words
        split_row = row['clean_question'].split(" ")
        # if the word is in the clean_question checking whether or not it is high value
        if word in split_row:
            if row['high_value'] == 1:
                high_count += 1
            else:
                low_count += 1
    return high_count, low_count                                  


# In[134]:


# Looking at values for comparison terms
observed_expected = [] 

comparison_terms = list(terms_used)[:5]

# getting the high and low count for each term 
for term in comparison_terms:
    high, low = term_value(term)
    observed_expected.append([high, low])

observed_expected


# ## Chi-squared Value

# In[137]:


from scipy.stats import chisquare
import numpy as np

# getting the total value counts 
high_value_count = jeopardy[jeopardy['high_value']==1].shape[0]
low_value_count = jeopardy[jeopardy['high_value']==0].shape[0]

# list for the chi-squared values
chi_squared = []

# Looping through the high and low value pairs
for pair in observed_expected:
    # finding the total observations
    total = sum(pair)
    # the proportion of the total
    total_prop = total/jeopardy.shape[0]
    # expected high and low values
    expected_high = total_prop * high_value_count
    expected_low = total_prop * low_value_count
    # creating arrays with the observed and expected values
    observed = np.array([pair[0], pair[1]])
    expeceted = np.array([expected_high, expected_low])
    chi_squared.append(chisquare(observed, expeceted))

chi_squared


# None of the results are statistically significant, this test also requires a higher number of observations in order for the test to be valid. 

# ## Future work 
# 
# - Find a more robust way to remove non-informative words
# - Delve more into the "Category" column
# - Look at the entire population
# 
