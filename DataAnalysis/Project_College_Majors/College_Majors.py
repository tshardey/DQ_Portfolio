
# coding: utf-8

# # Plotting Data
# 
# We'll be working with a dataset on the job outcomes of students who graduated from college between 2010 and 2012. The original data on job outcomes was released by American Community Survey, which conducts surveys and aggregates the data. FiveThirtyEight cleaned the dataset and released it on their Github repo.
# 
# ## Questions to be answered
# 
# 
#     Do students in more popular majors make more money?
#         Using scatter plots
#     How many majors are predominantly male? Predominantly female?
#         Using histograms
#     Which category of majors have the most students?
#         Using bar plots
# 

# In[2]:


# Setting up the workspace
import pandas as pd
import matplotlib as plt

get_ipython().magic('matplotlib inline')


# In[3]:


# Previewing Data
recent_grads = pd.read_csv("recent-grads.csv")
print(recent_grads.head())
print(recent_grads.tail())
recent_grads.describe()


# ## Scatter Plots

# In[4]:


# Removing null values 
raw_data_count = recent_grads.shape[0]
recent_grads = recent_grads.dropna()
cleaned_data_count = recent_grads.shape[0]
# Checking the number of null values removed
print("Number of columns removed:" + str(raw_data_count - cleaned_data_count))


# In[5]:


# Scatter Plots to look at correlation between columns
ax = recent_grads.plot(x='Sample_size', y='Median', kind='scatter', title='Sample Size vs. Median', figsize=(5,5))
ax1 = recent_grads.plot(x='Sample_size', y='Unemployment_rate', kind='scatter', title='Sample Size vs. Unemployment Rate', figsize=(5,5))
ax2 = recent_grads.plot(x='Full_time', y='Median', kind='scatter', title='Full time vs. Median', figsize=(5,5))
ax3 = recent_grads.plot(x='ShareWomen', y='Unemployment_rate', kind='scatter', title='Share Women vs. Unemployment Rate', figsize=(5,5))
ax4 = recent_grads.plot(x='Men', y='Median', kind='scatter', title='Men vs. Median', figsize=(5,5))
ax5 = recent_grads.plot(x='Women', y='Median', kind='scatter', title='Women vs. Median', figsize=(5,5))


# There is a weak postivive correlation between the sample size and median income.  The sample sizes tended to be on the lower end of the spectrum and thus have the most varied data.  There is no correlation between the percentage of women in a major and unemployment rate.   

# ## Histograms

# In[30]:


# Histograms to look at data distribution
ah = recent_grads['Sample_size'].hist(bins=20, range=(0,3000))
ah.set_title("Sample Size of full-time employees")


# In[31]:


ah1 = recent_grads['Median'].hist(bins=30, range=(20000,80000))
ah1.set_title("Median Salary")


# In[32]:


ah2 = recent_grads['Employed'].hist(bins=25, range = (0,200000))
ah2.set_title("Number Employed")


# In[33]:


ah3 = recent_grads['Full_time'].hist(bins=25, range = (0,200000))
ah3.set_title("Number employed 35 hours or more")


# In[36]:


ah4 = recent_grads['ShareWomen'].hist(bins=10)
ah4.set_title("Percentage of women graduates")


# In[37]:


ah5 = recent_grads['Unemployment_rate'].hist(bins=20)
ah5.set_title("Unemployment Rate")


# In[38]:


ah6 = recent_grads['Men'].hist(bins=40, range = (0,100000))
ah6.set_title("Male graduates")


# In[39]:


ah7 = recent_grads['Women'].hist(bins=40, range = (0,100000))
ah7.set_title("Female graduates")


# The mode for the median salary was about \$35k.  Over half of all majors are predominately male.  The mode for unemployment rate was around 0.06%.  

# ## Scatter-Matrix Plots

# In[28]:


# Importing scatter-matrix from pandas plotting
from pandas.tools.plotting import scatter_matrix


# In[48]:


df= recent_grads[['Sample_size', 'Median']]
sm = scatter_matrix(df, figsize = (4,4))


# In[47]:


df1= recent_grads[['Sample_size', 'Median', 'Unemployment_rate']]
sm1 = scatter_matrix(df1, figsize = (6,6))


# In[50]:


df2= recent_grads[['Men', 'Median', 'Women']]
sm2 = scatter_matrix(df2, figsize = (6,6))


# In[53]:


df3= recent_grads[['ShareWomen', 'Unemployment_rate', 'Median']]
sm3 = scatter_matrix(df3, figsize = (6,6))


# There is a weak negative correlation between the number of women in a major and the median salary.  There is no correlation between the unemployment rate and the percentage of women in a major.  Median income is negatively skewed, as is any group based on the number of people.  

# ## Bar Plot

# In[58]:


recent_grads[:10].plot.bar(x='Major', y= 'ShareWomen')
recent_grads[len(recent_grads)-10:].plot.bar(x='Major', y= 'ShareWomen')


# In[59]:


recent_grads[:10].plot.bar(x='Major', y= 'Unemployment_rate')
recent_grads[len(recent_grads)-10:].plot.bar(x='Major', y= 'Unemployment_rate')


# In[61]:


recent_grads[:10].plot.bar(x='Major', y= ['Men', 'Women'])
recent_grads[len(recent_grads)-10:].plot.bar(x='Major', y= ['Men', 'Women'])


# ## Box Plots

# In[71]:


recent_grads[['Unemployment_rate']].plot.box()
recent_grads[['Men', 'Women']].plot.box()
recent_grads[['Median']].plot.box()


# ## Hexagonal Bin Plot

# In[79]:


recent_grads.plot.hexbin(x='Low_wage_jobs', y='ShareWomen', gridsize = 10)

