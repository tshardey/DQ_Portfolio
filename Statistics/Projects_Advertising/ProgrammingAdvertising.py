
# coding: utf-8

# # Potential Online Programming Advertising Markets
# 
# ## Project Goals:
# 
# Find out markets would be best to advertise in for a new subscription service that offers Web and Mobile Development courses. 

# In[78]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# In[79]:


# Reading in the data
code_surveys = pd.read_csv("2017-fCC-New-Coders-Survey-Data.csv", low_memory=False)


# In[80]:


# Previewing the data
code_surveys.head()


# In[81]:


print("The shape of the data is:\n{}".format(code_surveys.shape))
print("The column names are:\n{}".format(code_surveys.columns))


# In[82]:


code_surveys.describe()


# ## Data Relevance
# For the purpose of our analysis, we want to answer questions about a population of new coders that are interested in the subjects we teach. We'd like to know:
# 
# - Where are these new coders located.
# - What are the locations with the greatest number of new coders.
# - How much money new coders are willing to spend on learning.
# 

# In[83]:


# Subsetting the job information
job_interests = code_surveys['JobRoleInterest']


# Since the JobRoleInterest column can contain multiple answers the data will be separated using the split() function over the common and appended to a new list for analysis.

# In[84]:


# Create an empty list to hold the separated job functions
jobs = []

# Loop through each iten in job_interest
for job in job_interests:
    # Check to see if it is of type string
    if type(job) is str:
        # Split the string and add the item to the list
        for item in job.split(","):
            jobs.append(item)
    # If it is not a string, ex. NaN, then just add
    else:
        jobs.append(job)


# In[85]:


# Uses the Counter function to count
# the appearance of each item and create a dictionary
job_series = pd.Series(jobs).value_counts().sort_values(ascending=False).reset_index()
job_series    


# In[86]:


# The job titles that have to deal with the web
web = job_series[job_series['index'].str.contains('Web')]
web


# In[87]:


# The job titles that have to deal with the mobile
mobile = job_series[job_series['index'].str.contains('Mobile')]
mobile


# Web Development and Mobile Development were the top 6 mentioned job interests in the frequency table.  

# In[88]:


# Subsetting the data to include those who marked interest in Web or Development
interested_coders = code_surveys[code_surveys["JobRoleInterest"].str.contains("Web|Mobile") == True].copy()


# In[89]:


countries_rel = interested_coders['CountryLive'].value_counts(normalize=True)
countries_abs = interested_coders['CountryLive'].value_counts()

pd.DataFrame(data={'Relative Frequency': countries_rel, 'Absolute Frequency': countries_abs})


# In[90]:


get_ipython().magic('matplotlib inline')
plt.style.use("fivethirtyeight")
countries.head().plot.bar()
plt.ylabel("Percentage \%")
plt.xlabel("Country")
plt.title("Top 5 Countries")


# Participation of the survey, from individiduals are interested in mobile or web development, is approximately 45% from people who live in the United States of America, with about 7% from India.  As FreeCodeCamp courses are in English, and four out of the top 5 countries have English as a primary language, these would be a good place to start advertising in.  

# In[91]:


# Subsetting data to only look at the top 4 countries
interested_countries = interested_coders[interested_coders['CountryLive'].isin(countries.head(4).index)].copy()


# In[92]:


print("The shape of the df:{}".format(interested_countries.shape))
# Replacing zero values in the MonthsProgramming column
interested_countries["MonthsProgramming"] = interested_countries["MonthsProgramming"].replace(0,1)
# Adding a column to calculate the money spent
interested_countries["MoneyPerMonth"] = interested_countries["MoneyForLearning"]/interested_countries["MonthsProgramming"]
print("The number people who haven't spent money:{}".format(sum(interested_countries["MoneyPerMonth"].isna())))


# In[93]:


# Drop Null values
interested_countries.dropna(subset=["MoneyPerMonth"], inplace=True)
# Checking that null values were dropped
print("The number people who haven't spent money:{}".format(sum(interested_countries["MoneyPerMonth"].isna())))


# In[94]:


money_country = interested_countries.groupby('CountryLive').mean()
money_country['MoneyPerMonth'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]


# In[95]:


# Isolating the top 4 countries
top_4 = interested_countries[interested_countries['CountryLive'].str.contains(
'United States of America|India|United Kingdom|Canada')]


# In[96]:


import seaborn as sns
# Generating a box plot for each country for how much money is spent
sns.boxplot(y='MoneyPerMonth', x='CountryLive', data=top_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()


# Based on the boxplots it looks like there are some large outliers for the US and India that may need to be removed. The outliers for the US will be removed first to get a better look at India.  It is highly improbable that individuals spent more than $20,000/month on non-tuition related courses.

# In[97]:


# Removing extreme outliers
top_4 = top_4[top_4['MoneyPerMonth']<20000]


# In[98]:


# Generating a box plot for each country for how much money is spent
sns.boxplot(y='MoneyPerMonth', x='CountryLive', data=top_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()


# In[100]:


# Looking at the top values in India
india_outliers = top_4[(top_4['CountryLive']=='India')&(top_4['MoneyPerMonth']>2000)]
india_outliers


# There are 6 values in India over $2,000/month, which is an unusual amount to spend on education outside of University.  Participants of bootcamps could spend that much per month, but none of these survey takers participated in a bootcamp.  It is probably safe to remove these values.

# In[102]:


# Drop India Outliers
top_4.drop(india_outliers.index, inplace=True)


# In[103]:


money_country_new = top_4.groupby('CountryLive').mean()
money_country_new['MoneyPerMonth'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]


# In[106]:


top_4['CountryLive'].value_counts(normalize=True)


# The bulk of the advertising budget should go to the US, as individuals spend almost double of any other country,and has the highest participation.  The second country to advertise in should be India, as they are willing to pay at least the subscription cost and have double the potential subscribers.  
