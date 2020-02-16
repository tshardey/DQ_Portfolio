
# coding: utf-8

# # Plot Aesthetics 
# 
# ## STEM Plots 

# In[1]:


get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt

# Importing Data
women_degrees = pd.read_csv('percent-bachelors-degrees-women-usa.csv')
# Setting color values
cb_dark_blue = (0/255,107/255,164/255)
cb_orange = (255/255, 128/255, 14/255)
# List of stem degrees
stem_cats = ['Engineering', 'Computer Science', 'Psychology', 'Biology', 'Physical Sciences', 'Math and Statistics']
# Setting the plot size
fig = plt.figure(figsize=(18, 3))

# Looping through each degree
for sp in range(0,6):
    # Defining the placement of the subplot
    ax = fig.add_subplot(1,6,sp+1)
    # Plotting STEM degree data for men and women by year
    ax.plot(women_degrees['Year'], women_degrees[stem_cats[sp]], c=cb_dark_blue, label='Women', linewidth=3)
    ax.plot(women_degrees['Year'], 100-women_degrees[stem_cats[sp]], c=cb_orange, label='Men', linewidth=3)
    # Removing spines for each subplot
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)
    # Setting x and y axis limits for each subplot
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0,100)
    # Adding a descriptive title to each subplot
    ax.set_title(stem_cats[sp])
    # Removing ticks from each subplot
    ax.tick_params(bottom="off", top="off", left="off", right="off")
    
    # Adding descriptive label text to the first and last subplot in a column
    if sp == 0:
        ax.text(2005, 87, 'Men')
        ax.text(2002, 8, 'Women')
    elif sp == 5:
        ax.text(2005, 62, 'Men')
        ax.text(2001, 35, 'Women')
        
plt.show()


# ## Other Degree Categories 

# In[11]:


# Degree categories
stem_cats = ['Psychology', 'Biology', 'Math and Statistics', 'Physical Sciences', 'Computer Science', 'Engineering']
lib_arts_cats = ['Foreign Languages', 'English', 'Communications and Journalism', 'Art and Performance', 'Social Sciences and History']
other_cats = ['Health Professions', 'Public Administration', 'Education', 'Agriculture','Business', 'Architecture']

# Combining all of the degree categories into a single list of lists
all_cats = [stem_cats, lib_arts_cats, other_cats]

# Creating an empty subplot and setting the desired size
fig, ax = plt.subplots(6,3, figsize=(12, 18))

# Looping through the high level degree categories
for cat in all_cats:
    # Looping through the degrees in each category
    for sp in range(0, len(cat)):
        # Line plot comparing of year vs degree for men and women
        ax[sp,all_cats.index(cat)] .plot(women_degrees['Year'], women_degrees[cat[sp]], c=cb_dark_blue, label='Women', linewidth=3)
        ax[sp,all_cats.index(cat)].plot(women_degrees['Year'], 100-women_degrees[cat[sp]], c=cb_orange, label='Men', linewidth=3)
        # Hiding spines for each subplot
        ax[sp,all_cats.index(cat)].spines["right"].set_visible(False)    
        ax[sp,all_cats.index(cat)].spines["left"].set_visible(False)
        ax[sp,all_cats.index(cat)].spines["top"].set_visible(False)    
        ax[sp,all_cats.index(cat)].spines["bottom"].set_visible(False)
        # Setting the x and y value limits for each subplot
        ax[sp,all_cats.index(cat)].set_xlim(1968, 2011)
        ax[sp,all_cats.index(cat)].set_ylim([0,100])
        # Limiting ticks to first and last tick mark to reduce clutter
        ax[sp,all_cats.index(cat)].set_yticks([0,100])
        # Creating a title for each subplot 
        ax[sp,all_cats.index(cat)].set_title(cat[sp])
        # Removing ticks from each subplot 
        ax[sp,all_cats.index(cat)].tick_params(bottom="off", top="off", left="off", right="off", labelbottom='off')
        # Adding in a gray line to easily determine a 50/50 gender gap
        ax[sp,all_cats.index(cat)].axhline(50, c=(171/255, 171/255, 171/255), alpha=0.3)
        # adding x labs to the last subplot in the figure
        if sp == len(cat)-1:
            ax[sp,all_cats.index(cat)].tick_params(labelbottom ='on')
            
        # Adding descriptive text to the first and last plot in the column
        if sp == 0:
            ax[sp,all_cats.index(cat)].text(2005, 87, 'Men')
            ax[sp,all_cats.index(cat)].text(2002, 8, 'Women')
        elif sp == 5:
            ax[sp,all_cats.index(cat)].text(2005, 62, 'Men')
            ax[sp,all_cats.index(cat)].text(2001, 35, 'Women')
# Hiding the empty subplot created by one of the degree categories only 
# having 5 degrees.
ax[5,1].set_visible(False)
plt.savefig('gender_degrees.png')
plt.show()

