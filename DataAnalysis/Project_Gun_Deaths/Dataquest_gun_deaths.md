
# Gun Deaths Evaluation 

## Importing guns.csv using csv module


```python
import csv
f = open("guns.csv", "r")
data = list(csv.reader(f))
```

## Data Cleaning

The first step of the data cleaning process was to capture the headers in a variable "headers" and to remove it from the data set to be evaluated.  


```python
headers = data[0]
data = data[1:]
```

## Initial Analysis 

The number of gun deaths per year in the US was determined to get a general view of some of the data at hand.  
This was done by:

- Creating an empty list
- Looping through the rows in the gun deaths data and appending just the year column to the empty list "years"
- An empty dictionary was created
- The new list "years" was looped through and each instance was counted.  


```python
years = []
for death in data:
    years.append(death[1])

year_counts = {}
for year in years:
    if year in year_counts:
        year_counts[year] += 1
    else:
        year_counts[year] = 1

print("Dictionary of gun deaths per year (2012-2014):")        
print(year_counts)
```

    Dictionary of gun deaths per year (2012-2014):
    {'2014': 33599, '2012': 33563, '2013': 33636}


## Looking at Dates and Times

In order to clean up the time component of the data, the datetime module was imported.  

- An empty list was created to house the dates
- For each row in the gun death data, a datetime object was created using the year and month columns of the dataset
- An empty dictionary was created to house the datetime counts
- The dates list was looped through and each instance of a month/year was counted.  


```python
import datetime

dates = []
for row in data:
    dates.append(datetime.datetime(year = int(row[1]), month = int(row[2]), day = 1))

date_counts = {}
for date in dates:
    if date in date_counts:
        date_counts[date] += 1
    else:
        date_counts[date] = 1

print("\nDictionary of Gun Deaths per Month/Year:")        
print(date_counts)
```

    
    Dictionary of Gun Deaths per Month/Year:
    {datetime.datetime(2014, 12, 1, 0, 0): 2857, datetime.datetime(2014, 2, 1, 0, 0): 2361, datetime.datetime(2013, 5, 1, 0, 0): 2806, datetime.datetime(2012, 3, 1, 0, 0): 2743, datetime.datetime(2012, 8, 1, 0, 0): 2954, datetime.datetime(2012, 5, 1, 0, 0): 2999, datetime.datetime(2012, 12, 1, 0, 0): 2791, datetime.datetime(2014, 4, 1, 0, 0): 2862, datetime.datetime(2014, 7, 1, 0, 0): 2884, datetime.datetime(2013, 3, 1, 0, 0): 2862, datetime.datetime(2013, 2, 1, 0, 0): 2375, datetime.datetime(2012, 1, 1, 0, 0): 2758, datetime.datetime(2012, 2, 1, 0, 0): 2357, datetime.datetime(2013, 12, 1, 0, 0): 2765, datetime.datetime(2013, 4, 1, 0, 0): 2798, datetime.datetime(2013, 9, 1, 0, 0): 2742, datetime.datetime(2014, 5, 1, 0, 0): 2864, datetime.datetime(2012, 4, 1, 0, 0): 2795, datetime.datetime(2012, 11, 1, 0, 0): 2729, datetime.datetime(2013, 11, 1, 0, 0): 2758, datetime.datetime(2013, 7, 1, 0, 0): 3079, datetime.datetime(2013, 10, 1, 0, 0): 2808, datetime.datetime(2012, 10, 1, 0, 0): 2733, datetime.datetime(2014, 8, 1, 0, 0): 2970, datetime.datetime(2014, 3, 1, 0, 0): 2684, datetime.datetime(2012, 7, 1, 0, 0): 3026, datetime.datetime(2013, 8, 1, 0, 0): 2859, datetime.datetime(2014, 1, 1, 0, 0): 2651, datetime.datetime(2013, 6, 1, 0, 0): 2920, datetime.datetime(2014, 10, 1, 0, 0): 2865, datetime.datetime(2014, 11, 1, 0, 0): 2756, datetime.datetime(2012, 6, 1, 0, 0): 2826, datetime.datetime(2014, 6, 1, 0, 0): 2931, datetime.datetime(2012, 9, 1, 0, 0): 2852, datetime.datetime(2013, 1, 1, 0, 0): 2864, datetime.datetime(2014, 9, 1, 0, 0): 2914}


## Looking at Sex and Race Components

The same procedure for getting the number of gun deaths per year was applied to get the number of gun deaths per gender and per race.  It was simplified to exclude the intermediate list.  

- Creating an empty dictionary
- Looping through the rows in the gun deaths data 
- Adding the value for each row corresponding to either the sex or race to the dictionary as the key.  
- Counting the instance each sex key or race key appears.  


```python
sex_counts = {}

for row in data:
    if row[5] in sex_counts:
        sex_counts[row[5]] += 1
    else:
        sex_counts[row[5]] = 1

print("\nDictionary of gun deaths based on gender:")        
print(sex_counts)

race_counts = {}

for row in data:
    if row[7] in race_counts:
        race_counts[row[7]] += 1
    else:
        race_counts[row[7]] = 1

print("\nDictionary of gun deaths based on race:")        
print(race_counts)
```

    
    Dictionary of gun deaths based on gender:
    {'M': 86349, 'F': 14449}
    
    Dictionary of gun deaths based on race:
    {'Native American/Native Alaskan': 917, 'Hispanic': 9022, 'Asian/Pacific Islander': 1326, 'White': 66237, 'Black': 23296}


## Importing Census Data

To gain a more useful insight from the number of deaths per each race group, census data was imported via the csv module.  


```python
g = open("census.csv", "r")

census = list(csv.reader(g))
print("\nList of census data")
print(census)
```

    
    List of census data
    [['Id', 'Year', 'Id', 'Sex', 'Id', 'Hispanic Origin', 'Id', 'Id2', 'Geography', 'Total', 'Race Alone - White', 'Race Alone - Hispanic', 'Race Alone - Black or African American', 'Race Alone - American Indian and Alaska Native', 'Race Alone - Asian', 'Race Alone - Native Hawaiian and Other Pacific Islander', 'Two or More Races'], ['cen42010', 'April 1, 2010 Census', 'totsex', 'Both Sexes', 'tothisp', 'Total', '0100000US', '', 'United States', '308745538', '197318956', '44618105', '40250635', '3739506', '15159516', '674625', '6984195']]


## Census Data and Mapping

The census data was imported in a way that was not easy to view.  To rememedy this a dictionary was created to house the data.  The goal was to be able to reference the data directly when creating a mapping dictionary.  

The mapping dictionary was created using the values of the census data that corresponded to the race tags used in the gun death data.  

Ultimately I think there is a way where the census dictionary created could be cleaned up to use it directly as the mapping dictionary.  


```python
census_dict = {}
census_headers = census[0]
census_body = census[1]

for i in range(0, len(census_headers)):
    census_dict[census_headers[i]] = census_body[i]

mapping = {
    "Asian/Pacific Islander": 674625 + 15159516 ,
    "Black": 40250635, 
    "Native American/Native Alaskan":3739506,
    "Hispanic": 308745538,
    "White": 197318956,
}

print("\nMapping dictionary - reassigning census data to gun death race labels:")
print(mapping)
```

    
    Mapping dictionary - reassigning census data to gun death race labels:
    {'Hispanic': 308745538, 'White': 197318956, 'Asian/Pacific Islander': 15834141, 'Native American/Native Alaskan': 3739506, 'Black': 40250635}


## Race Deaths Per Capita (100k)

A new dictionary was created to house the porportion of race deaths per 100k of individuals within that race populatin.  This was done by:
- iterating through the key value pairs in the race_counts dictionary
- setting the key for race_per_hundredk to the same value as race_counts
- dividing the value of the race_counts, by the corresponding population for that key to get the per capita number
- multiplying the fraction by 100,000


```python
race_per_hundredk = {}

for key, value in race_counts.items():
    race_per_hundredk[key] = value/mapping[key] * 100000

print("\nDictionary of gun deaths per race per 100k individuals:")
print(race_per_hundredk)
```

    
    Dictionary of gun deaths per race per 100k individuals:
    {'Hispanic': 2.922147493512927, 'White': 33.56849303419181, 'Asian/Pacific Islander': 8.374309664161762, 'Native American/Native Alaskan': 24.521955573811088, 'Black': 57.8773477735196}


## Looking at Intent 

To look at the number of gun deaths per race that were homicides a new race count dictionary was created to house the race deaths that were homicides.  This was done by:
- Creating empty lists for the intent column
- Creating an empty list for the races column
- Creating an empty dictionary for the homicide race counts
- Iterating through races and checking whether the corresponding intents column was = "Homicide" using the enumerate function
- If the intent was homicide the race value was used as the key and incremented by one each time it appeared.  

Once this data was collected, a similar procedure could be used to determine the number of race deaths that are homicides per 100k individuals.  


```python
intents = [] 
for row in data:
    intents.append(row[3])

races = []
for row in data:
    races.append(row[7])

homicide_race_counts = {}
for i, value in enumerate(races):
    if intents[i] == "Homicide":
        if value in homicide_race_counts:
            homicide_race_counts[value] += 1
        else:
            homicide_race_counts[value] =1

print("\nDictionary of gun related homicides by race:")            
print(homicide_race_counts)

homicide_per_hundredk = {}

for key, value in homicide_race_counts.items():
    homicide_per_hundredk[key] = value/mapping[key] * 100000

print("\nDictionary of homicides by race per 100k individuals:")
print(homicide_per_hundredk)
```

    
    Dictionary of gun related homicides by race:
    {'Native American/Native Alaskan': 326, 'Hispanic': 5634, 'Asian/Pacific Islander': 559, 'White': 9147, 'Black': 19510}
    
    Dictionary of homicides by race per 100k individuals:
    {'Hispanic': 1.8248036996732242, 'White': 4.6356417981453335, 'Asian/Pacific Islander': 3.530346230970155, 'Native American/Native Alaskan': 8.717729026240365, 'Black': 48.471284987180944}


# Conclusions

- When looking at the sex variable for gun deaths, "Male" was associated with a much higher number of gun deaths.  As the population of males and females in a population are approximately equal, this was not divided by the census data.  
    -Using the census data to standardize the sex counts could be interesting to see how they vary
- When just looking at the number of gun deaths per race, "White" resulted in a substantially higher number than any other race group.  
- When this was adjusted per 100k individuals in the population, the race category "Black" had the highest number of gun deaths, and "White" dropped to third.  
- Intent indicated a much higher rate of deaths for the 'Black' category were homicides than other race categories.  
    -~48 deaths per 100k were homicide out of the total ~57 deaths per 100k 
    
## Future work

Analyze: 
- the number of gun deaths that are homicide depending on sex
- gun deaths that are suicide by both race and sex
- Look at education level against intent and race
- The number of police involved shooting by race and sex

A lot of the analysis is requires a very similar process, a function could simplify this analysis to be able to more quickly analyze the data.  

## Looking at Suicides by Race

The same process was followed to get the number of suicides by race as was used to determine the number of homicides per race


```python
suicide_race_counts = {}
for i, value in enumerate(races):
    if intents[i] == "Suicide":
        if value in suicide_race_counts:
            suicide_race_counts[value] += 1
        else:
            suicide_race_counts[value] =1
print("\nDictionary of suicides by race:")
print(suicide_race_counts)

suicide_per_hundredk = {}

for key, value in suicide_race_counts.items():
    suicide_per_hundredk[key] = value/mapping[key] * 100000
print("\nDictionary of suicides by race per 100k individuals:")
print(suicide_per_hundredk)
```

    
    Dictionary of suicides by race:
    {'Native American/Native Alaskan': 555, 'Hispanic': 3171, 'Asian/Pacific Islander': 745, 'White': 55372, 'Black': 3332}
    
    Dictionary of suicides by race per 100k individuals:
    {'Hispanic': 1.0270593772921182, 'White': 28.06217969245692, 'Asian/Pacific Islander': 4.705023152187416, 'Native American/Native Alaskan': 14.841532544673013, 'Black': 8.278130270491385}


## Homicides and Education Level

The number of homicides for each level of education was looked at.  Code used to analyze the number of homicides per race was altered to iterate through the education levels.  


```python
education = []
for row in data:
    education.append(row[10])

education_homicide_counts = {}
for i, value in enumerate(education):
    if intents[i] == "Homicide":
        if value in education_homicide_counts:
            education_homicide_counts[value] += 1
        else:
            education_homicide_counts[value] =1
print("\nDictionary of homicides by education level - \n(5 is highest level of education):")
print(sorted(education_homicide_counts.items()))
```

    
    Dictionary of homicides by education level - 
    (5 is highest level of education):
    [('1', 11839), ('2', 15649), ('3', 5640), ('4', 1559), ('5', 455), ('NA', 34)]


## Developing a Function

To simplfy repetative parts of the analysis a function was developed.  It takes:
- A dataset without headers
- The index for the column of the data which will form the main variable of interest.  
- The index for the column of data which will be used to subset the main variable
- The name of the subset that you want to analyze

This was used to find the police involved shootings per race and the number of race shootings that occured at the individuals home.


```python
def countFunction(dataSet, index1, index2, name):
    field1 = []
    field2 = []
    dictionary_output = {}
    for row in dataSet:
        field1.append(row[index1])
        field2.append(row[index2])
    for i, value in enumerate(field1):
        if field2[i] == name:
            if value in dictionary_output:
                dictionary_output[value] += 1
            else:
                dictionary_output[value] = 1   
    return dictionary_output


police_race_counts = countFunction(data, 7, 4, "1")
print("\nDictionary of police involved deaths by race:")
print(police_race_counts)

location_race_counts = countFunction(data, 7, 9, "Home")
print("\nDictionary of gun deaths that occured at home by race:")
print(location_race_counts)
```

    
    Dictionary of police involved deaths by race:
    {'Native American/Native Alaskan': 25, 'Hispanic': 282, 'Asian/Pacific Islander': 30, 'White': 709, 'Black': 356}
    
    Dictionary of gun deaths that occured at home by race:
    {'Native American/Native Alaskan': 592, 'Hispanic': 4310, 'Asian/Pacific Islander': 696, 'White': 45946, 'Black': 8942}

