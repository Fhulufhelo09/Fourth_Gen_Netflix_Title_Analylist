import pandas as pd
from datetimne import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
netflixdata=pd.read_csv(r"C:\Users\hp\Desktop\netflix\netflix_titles.csv")

#STEP1
#checking distribution of empty values
print("ouput missing values distribution")
print(netflixdata.isnull().mean())
print("")

#STEP2
# getting all the columns with string/mixed type values
str_column=list(netflixdata.columns)
str_column.remove('release_year')

# removing leading and trailing characters from columns with string datatype

for i in str_column:
    netflixdata[i]=netflixdata[i].str.strip()

    columns = ['director', 'cast', 'country', 'rating', 'date_added']

#STEP3
# looping through the columns to fill the entries with NaN values with empyt ("")
for column in columns:
    netflixdata[column] = netflixdata[column].fillna("")
    
    
netflixdata.head() 
#STEP4
# examining rows with null values for date_added column
rows = []

for i in range(len(netflixdata)):
    if netflixdata['date_added'].iloc[i] == "":
        rows.append(i)
        
# examine those rows to confirm null state
netflixdata.loc[rows, :] 

# extracting months added and years added
month_added = []
year_added = []

for i in range(len(netflixdata)):
    # replacing NaN values with 0
    if i in rows:
        month_added.append(0)
        year_added.append(0)
    else:
        date=str(netflixdata['date_added'].iloc[i]).split(" ")
        #date = list()
        month_added.append(date[0])
        year_added.append(int(date[2]))
        
# turning month names into month numbers
for i, month in enumerate(month_added): 
    if month != 0:
        datetime_obj = datetime.strptime(month, "%B")
        month_number = datetime_obj.month
        month_added[i] = month_number

# checking all months
print(set(month_added))
print(set(year_added))      

# inserting the month and year columns into the dataset
netflixdata.insert(7, "month_added", month_added, allow_duplicates = True)
netflixdata.insert(8, "year_added", year_added, allow_duplicates = True)
netflixdata.head()

#STEP5
#remove  columnS
netflixdata=netflixdata.drop(['director','cast','date_added'],axis=1)
netflixdata

#STEP6
#CREATE TWO DATA SET TVSHOWS AND FILMS
# looping through the dataset to identify rows that are TV shows and films
shows=[]
films=[]
for i in range(len(netflixdata)):
    if netflixdata['type'].iloc[i] == "TV Show":
        shows.append(i)
    else:
        films.append(i)
        
# grouping rows that are TV shows
netflixshows = netflixdata.loc[shows, :]

#grouping rows that are films
netflixfilms = netflixdata.loc[films, :]

# reseting the index of the new datasets
netflixshows = netflixshows.set_index([pd.Index(range(0, len(netflixshows)))])
netflixfilms = netflixfilms.set_index([pd.Index(range(0, len(netflixfilms)))]) 

#STEP7
# get length of movie or number of seasons of show
def getDuration(data):
    count = 0
    durations = []
    for value in data:
	# filling in missing values
        if type(value) is float:
            durations.append(0)
        else:
            values = value.split(" ")
            durations.append(int(values[0]))
    return durations

#STEP8
# inserting new SEASON type column for shows (renamed column)
netflixshows.insert(9, 'seasons', getDuration(netflixshows['duration']))
netflixshows = netflixshows.drop(['duration'], axis = 1)
netflixshows.head()

#STEP9
# inserting new LENGTH type column for films (renamed column)
netflixfilms.insert(9, 'length', getDuration(netflixfilms['duration']))
netflixfilms = netflixfilms.drop(['duration'], axis = 1)
netflixfilms.head()

#STEP10
# getting the unique ratings for films
netflixfilms['rating'].unique()

#STEP11# printing more details of the rows that have WRONG ratings
wrong_ratings = ['74 min', '84 min', '66 min']
for i in range(len(netflixfilms)):
    if netflixfilms['rating'].iloc[i] in wrong_ratings:
        print(netflixfilms.iloc[i])
        print("")

#STEP11
# getting the row indices


index = [3562, 3738, 3747]


# fixing the entries
for i in index:
    split_value = netflixfilms['rating'].iloc[i].split(" ")
    minutes = split_value[0]
   
    netflixfilms['length'].iloc[i] =  minutes
   
    netflixfilms['length']= netflixfilms['length'].astype(int)
    netflixfilms['rating'].iloc[i] = "NR"
    
# double checking the entries again
for i in index:
    print(netflixfilms.iloc[i])

#STEP12
# # fixing the entries in rating
for i in range(len(netflixfilms)):
    if netflixfilms['rating'].iloc[i] == "":
         netflixfilms['rating']=netflixfilms['rating'].replace("","NR")    
        
#STEP13
#looking into my data again to see more 0 ENRTY
select_prod = netflixshows.loc[netflixshows['year_added'] == 0]

print(select_prod)   

#STEP14
#FINDING MEAN TO REPLACE ZERO ENTRIES
netflixshows['year_added'].mean()
netflixshows['month_added'].mean()

#STEP15
#REPLACING ZERO ENTRIES USING THE MEAN
netflixshows['year_added']=netflixshows['year_added'].replace(0,2011)
netflixshows['month_added']=netflixshows['month_added'].replace(0,6)

#STEP 16
#CREATING VISUAL ABOUT SEASON, LENGTH, YEAR ADDED ,YEAR RELEASED,type
# updated visuals
#scatter plots
netflixshows.plot(kind = 'scatter', x = 'release_year', y = 'seasons')
plt.show()
netflixfilms.plot(kind = 'scatter', x = 'release_year', y = 'length')
plt.show()

#checking the mean,median and quartiles of the movies
sns.catplot(data=netflixfilms, x='type', y='release_year', kind='box')
plt.show()
#checking the mean,median and quartiles of the TV shows
sns.catplot(data=netflixshows, x='type', y='release_year', kind='box')
plt.show()

#checking the duration mean ,median and quartiles of the movies
sns.catplot(data=netflixfilms, x='type', y='length', kind='box')
plt.show()

#checking the duration  mean ,median and quartiles of the Tv shows
sns.catplot(data=netflixshows, x='type', y='seasons', kind='box')
plt.show()

#checking the duration of the TV shows
sns.catplot(data=netflixshows, x='rating', y='seasons', kind='bar')
plt.show()


#checking the duration of the TV shows
sns.catplot(data=netflixfilms, x='rating', y='length', kind='bar')
plt.show()

#counting categories in rating of the movies 
sns.countplot(data=netflixfilms, x='rating')
plt.show()

#counting categories in rating of the movies 
sns.countplot(data=netflixshows, x='rating')
plt.show()

#piechart for rating movies in percentage
netflixfilms.groupby('rating').size().plot(kind='pie', autopct='%.2f')

#piechart for rating movies in percentage

netflixshows.groupby('rating').size().plot(kind='pie', autopct='%.2f')