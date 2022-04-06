from email.utils import parsedate_to_datetime
import pandas as pd
import time
import numpy as np

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
    dataframe = dataframe[dataframe['Distance(mi)']!=0].dropna()
    return dataframe

def cleanTimes(dataframe):
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    dataframe['End_Time'] = pd.to_datetime(dataframe['End_Time'])
    start = dataframe['Start_Time']
    end = dataframe['End_Time']
    dataframe['Difference'] = end - start
    dataframe = dataframe[dataframe['Difference']!=0].dropna()
    return dataframe

def fullClean(dataframe):
    x = clean(dataframe)
    x = cleanIfMoreThanThreeNaN(x)
    x = cleanDistance(x)
    x = cleanTimes(x)
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

def q2(dataframe):
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    #Clean column from the time stamps
    dataframe['Start_Dates'] = dataframe['Start_Time'].dt.date
    #Convert to string
    dataframe['Strings'] = dataframe['Start_Dates'].astype(str)
    #Remove last 6 characters from strings
    dataframe['Years'] = dataframe['Strings'].str[:-6]
    for x in dataframe['Years']:
        if x == '2020':
            answer = dataframe['State'].mode().to_string(index=False)
            break
    return answer

def q3(dataframe):
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    #Clean column from the time stamps
    dataframe['Start_Dates'] = dataframe['Start_Time'].dt.date
    #Convert to string
    dataframe['Strings'] = dataframe['Start_Dates'].astype(str)
    #Remove first 5 and last 3 characters from strings
    dataframe['Years'] = dataframe['Strings'].str[:-6]
    for x, y in zip(dataframe['Years'], dataframe['Severity']):
        if x == '2021' and y == 2:
            answer = dataframe['State'].mode().to_string(index=False)
            break
    return answer

def q4(dataframe):
    c1, c2, c3 = 0, 0, 0
    for x, y in zip(dataframe['State'], dataframe['Severity']):
        if x == 'VA' and y == 1:
            c1 += 1
        elif x == 'VA' and y == 2:
            c2 += 1
        elif x == 'VA' and y == 3:
            c3 +=1
    if c1 > c2 and c1 > c3:
        return 'Severity 1'
    elif c2 > c1 and c2 > c3:
        return 'Severity 2'
    elif c3 > c1 and c3 > c2:
        return 'Severity 3' 

def q5(dataframe):
    states = dataframe.loc[dataframe['State'] == 'CA', 'City']
    return states.value_counts()[:5].index.tolist()

def q6(dataframe):
    temp = dataframe['Temperature(F)']
    hum = dataframe['Humidity(%)']
    for x in dataframe['Severity']:
        if x == 4:
            return "Temperature: {}   Humidity: {}".format(round(temp.mean(), 3), round(hum.mean(), 3))

def q7(dataframe):
    weather = dataframe['Weather_Condition']
    return weather.value_counts()[:3].index.tolist()

def q8(dataframe):
    visibility = dataframe['Visibility(mi)']
    severity = dataframe['Severity']
    state = dataframe['State']
    for x, y, z in zip(state, severity, visibility):
        if x == 'NH' and y == 2:
            return np.max(z)

def q9(dataframe):
    c1 = 0
    c2 = 0
    c3 = 0
    for x, y in zip(dataframe['City'], dataframe['Severity']):
        if x == 'Bakersfield' and y == 1:
            c1 += 1
        elif x == 'Bakersfield' and  y == 2:
            c2 += 1
        elif x == 'Bakersfield' and y == 3:
            c3 += 1   
    return "Severity 1: {}   Severity 2: {}   Severity 3: {}".format(c1, c2, c3)

def q10(dataframe):
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    dataframe['End_Time'] = pd.to_datetime(dataframe['End_Time'])
    #What was the longest accident (in hours) recorded in Florida in the Spring (March, April, and May) of 2022?
    for x,y,z in zip(dataframe['State'], dataframe['Start_Time'], dataframe['End_Time']):
        if x == 'FL' and y.month in (3, 4, 5) and z.month in (3,4,5) and y.year == 2021 and z.year == 2021:
            return z - y


print("Current time[{} seconds] Performing full data clean up".format(round(time.time()-start, 2)))
data = fullClean(data)

print("Current time[{} seconds] Row count after cleaning: {}".format(round(time.time()-start, 2), len(data)))
#template for copy paste print("Current time[{} seconds]".format(round(time.time()-start, 2)))

#Question 1
print("Current time[{} seconds] In what month were there more accidents reported? {}".format(round(time.time()-start, 2), q1(data)))

#Question 2
print("Current time[{} seconds] What is the state that had the most accidents in 2020? {}".format(round(time.time()-start, 2), q2(data)))

#Question 3
print("Current time[{} seconds] What is the state that had the most accidents of severity 2 in 2021? {}".format(round(time.time()-start, 2), q3(data)))

#Question 4
print("Current time[{} seconds] What severity is the most common in Virginia? {}".format(round(time.time()-start, 2), q4(data)))

#Question 5
print("Current time[{} seconds] What are the 5 cities that had the most accidents in 2019 in California? {}".format(round(time.time()-start, 2), q5(data)))

#Question 6
print("Current time[{} seconds] What was the average humidity and average temperature of all accidents of severity 4 that occurred in 2021? {}".format(round(time.time()-start, 2), q6(data)))

#Question 7
print("Current time[{} seconds] What are the 3 most common weather conditions (weather_conditions) when accidents occurred? {}".format(round(time.time()-start, 2), q7(data)))

#Question 8
print("Current time[{} seconds] What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire? {}".format(round(time.time()-start, 2), q8(data)))

#Question 9
print("Current time[{} seconds] How many accidents of each severity were recorded in Bakersfield? {}".format(round(time.time()-start, 2), q9(data)))

#Question 10
print("Current time[{} seconds] What was the longest accident (in hours) recorded in Florida in the Spring (March, April, and May) of 2022? {}".format(round(time.time()-start, 2), q10(data)))
