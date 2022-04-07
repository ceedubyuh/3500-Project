import pandas as pd
import time
import numpy as np

start = time.time()

def currTime():
    x = round(time.time()-start, 2)
    return x
    
print("Current time[{} seconds] Loading and cleaning input dataset".format(currTime()))
print("------------------------------------------------------------")
print("Current time[{} seconds] Starting script".format(currTime()))
print("Current time[{} seconds] Loading CSV".format(currTime()))

data = pd.read_csv('Us_Accidents_data.csv')

def clean(dataframe):
    #Clean if selected rows contain NaN
    return dataframe.dropna(axis=0, subset=('Zipcode', 'ID', 'Severity', 'Start_Time', 
    'End_Time', 'Visibility(mi)', 'Weather_Condition', 'Country'))

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

def cleanZips(dataframe):
    dataframe['Clean_Zips'] = dataframe['Zipcode'].str[:5]
    return dataframe

def fullClean(dataframe):
    x = clean(dataframe)
    x = cleanIfMoreThanThreeNaN(x)
    x = cleanDistance(x)
    x = cleanZips(x)
    x = cleanTimes(x)
    return x

def q1(dataframe):
    #Grab Start_Time column
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    return dataframe['Start_Time'].dt.month.mode().to_string(index=False)

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
    #Initialize counters
    c1, c2, c3, c4 = 0, 0, 0, 0
    #Get severity value from row if state value in the row is VA
    severity = dataframe.loc[dataframe['State'] == 'VA', 'Severity']
    #Loop through all severities and tally each
    for x in severity:
        if x == 1:
            c1 += 1
        elif x == 2:
            c2 += 1
        elif x == 3:
            c3 += 1
        elif x == 4:
            c4 += 1  
    if c1 > c2 and c1 > c3 and c1 > c4:
        return 'Severity 1'
    elif c2 > c1 and c2 > c3 and c2 > c4 :
        return 'Severity 2'
    elif c3 > c1 and c3 > c2 and c3 > c4:
        return 'Severity 3' 
    else:
        return 'Severity 4'

def q5(dataframe):
    #Get all cities if the state value in the row is CA
    cities = dataframe.loc[dataframe['State'] == 'CA', 'City']
    #Set years to all years
    years = data['Start_Time'].dt.year
    #Loop through them both 
    for x, y in zip(years, dataframe['State']):
        if x == 2019 and y == 'CA':
            return cities.value_counts()[:5].index.tolist()

def q6(dataframe):
    #Get temp and humidity columns
    temp = dataframe.loc[dataframe['Severity'] == 4, 'Temperature(F)']
    hum = dataframe.loc[dataframe['Severity'] == 4, 'Humidity(%)']
    return "Temperature: {}   Humidity: {}".format(round(temp.mean(), 3), round(hum.mean(), 3))

def q7(dataframe):
    weather = dataframe['Weather_Condition']
    return weather.value_counts()[:3].index.tolist()

def q8(dataframe):
    visibility = dataframe.loc[dataframe['State'] == 'NH', 'Visibility(mi)']
    return visibility.max()

def q9(dataframe):
    c1, c2, c3, c4 = 0, 0, 0, 0
    #Get all rows severity value were the rows city value is Bakersfield
    severity = dataframe.loc[dataframe['City'] == 'Bakersfield', 'Severity']
    for x in severity:
        if x == 1:
            c1 += 1
        elif x == 2:
            c2 += 1
        elif x == 3:
            c3 += 1
        elif x == 4:
            c4 += 1
    return "Severity 1: {}   Severity 2: {}   Severity 3: {}   Severity 4: {}".format(c1, c2, c3, c4)

def q10(dataframe):
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    dataframe['End_Time'] = pd.to_datetime(dataframe['End_Time'])
    for x,y,z in zip(dataframe['State'], dataframe['Start_Time'], dataframe['End_Time']):
        if x == 'FL' and y.month in (3, 4, 5) and z.month in (3,4,5) and y.year == 2021 and z.year == 2021:
            return z - y

print("Current time[{} seconds] \
Performing full data clean up".format(currTime()))
data = fullClean(data)
print("Current time[{} seconds] \
Row count after cleaning: {}" .format(currTime(), len(data)))
#Question 1
print("Current time[{} seconds] \
(Q1) In what month were there more accidents reported? {}".format(currTime(), q1(data)))
#Question 2
print("Current time[{} seconds] \
(Q2) What is the state that had the most accidents in 2020? {}".format(currTime(), q2(data)))
#Question 3
print("Current time[{} seconds] \
(Q3) What is the state that had the most accidents of severity 2 in 2021? {}".format(currTime(), q3(data)))
#Question 4
print("Current time[{} seconds] \
(Q4) What severity is the most common in Virginia? {}".format(currTime(), q4(data)))
#Question 5
print("Current time[{} seconds] \
(Q5) What are the 5 cities that had the most accidents in 2019 in California? {}".format(currTime(), q5(data)))
#Question 6
print("Current time[{} seconds] \
(Q6) What was the average humidity and average temperature of all accidents of severity 4 that occurred in 2021? {}".format(currTime(), q6(data)))
#Question 7
print("Current time[{} seconds] \
(Q7) What are the 3 most common weather conditions (weather_conditions) when accidents occurred? {}".format(currTime(), q7(data)))
#Question 8
print("Current time[{} seconds] \
(Q8) What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire? {}".format(currTime(), q8(data)))
#Question 9
print("Current time[{} seconds] \
(Q9) How many accidents of each severity were recorded in Bakersfield? {}".format(currTime(), q9(data)))
#Question 10
print("Current time[{} seconds] \
(Q10) What was the longest accident (in hours) recorded in Florida in the Spring (March, April, and May) of 2022? {}".format(currTime(), q10(data)))
