import pandas as pd
import numpy as np
import time

start = time.time()
print("Current time[{} seconds] Loading and cleaning input dataset".format(round(time.time()-start, 2)))
print("------------------------------------------------------------")
print("Current time[{} seconds] Starting script".format(round(time.time()-start, 2)))
print("Current time[{} seconds] Loading CSV".format(round(time.time()-start, 2)))

data = pd.read_csv('Us_Accidents_data.csv')

def clean(dataframe):
    #Clean if selected rows contain NaN
    return dataframe.dropna(axis=0, subset=('Zipcode', 'ID', 'Severity', 'Start_Time', 'End_Time', 'Visibility(mi)', 'Weather_Condition', 'Country'))

def cleanIfMoreThanThreeNaN(dataframe):
    #Drop rows that contain 3 or more NaN
    return dataframe.dropna(thresh = len(dataframe.columns) <= -3)
    
def cleanDistance(dataframe):
    #Drop rows of column 'Distance(mi)' that equal 0
    return dataframe.loc[data['Distance(mi)'] == 0]

def fullClean(dataframe):
    #Perform clean on temp 'x'
    x = clean(dataframe)
    #Perform cleanIfMoreThanThreeNaN on temp 'x' and set to temp 'y'
    x = cleanIfMoreThanThreeNaN(x)
    #Perform cleanDistance on temp 'y' and set to temp 'z'
    x = cleanDistance(x)
    #Return 'z'
    return x

def q1(dataframe):
    #Grab Start_Time column
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    #Clean column from the time stamps
    dataframe['Start_Dates'] = dataframe['Start_Time'].dt.date
    #Convert to string
    dataframe['Strings'] = dataframe['Start_Dates'].astype(str)
    #Remove first 5 and last 3 characters from strings
    dataframe['Months'] = dataframe['Strings'].str[5:-3]
    #Return the most occuring month, set index to false
    return dataframe['Months'].mode().to_string(index=False)


print("Current time[{} seconds] Performing full data clean up".format(round(time.time()-start, 2)))
data = fullClean(data)
print("Current time[{} seconds] Row count after cleaning: {}".format(round(time.time()-start, 2), len(data)))
#template for copy paste print("Current time[{} seconds]".format(round(time.time()-start, 2)))

#Question 1
print("Current time[{} seconds] In what month were there more accidents reported? {}".format(round(time.time()-start, 2), q1(data)))
