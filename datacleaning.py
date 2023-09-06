import pandas as pd
from datetimne import datetime
import matplotlib.pyplot as plt
netflixdata=pd.read_csv(r"C:\Users\hp\Desktop\netflix\netflix_titles.csv")

#checking distribution of empty values
print("ouput missing values distribution")
print(netflixdata.isnull().mean())
print("")

# getting all the columns with string/mixed type values
str_column=list(netflixdata.columns)
str_column.remove('release_year')

# removing leading and trailing characters from columns with str type

for i in str_column:
    netflixdata[i]=netflixdata[i].str.strip()