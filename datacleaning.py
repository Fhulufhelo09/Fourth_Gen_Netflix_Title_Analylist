import pandas as pd
from datetimne import datetime
import matplotlib.pyplot as plt
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
netflixshows.insert(11, 'seasons', getDuration(netflixshows['duration']))
netflixshows = netflixshows.drop(['duration'], axis = 1)
netflixshows.head()

#STEP9
# inserting new LENGTH type column for films (renamed column)
netflixfilms.insert(9, 'length', getDuration(netflixfilms['duration']))
netflixfilms = netflixfilms.drop(['duration'], axis = 1)
netflixfilms.head()