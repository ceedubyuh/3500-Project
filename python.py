# Course: CMPS 3500
# CLASS PROJECT
# Python data analysis
# 
# by:
# Carter Womack, 
# Jose Figueroa, 
# Stuart Wurtman, 
# Dylan Gonzalez
#
#desc: Python data analysis program
#      that cleans a dataset, and 
#      performs basic functions to
#      to display the data in various ways
import pandas as pd
import time


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
    #Set Start and End time columns to datetimes
    dataframe['Start_Time'] = pd.to_datetime(dataframe['Start_Time'])
    dataframe['End_Time'] = pd.to_datetime(dataframe['End_Time'])
    #Declare new datetimes as variables
    #(not necessary, just easier to read in function)
    start = dataframe['Start_Time']
    end = dataframe['End_Time']
    #Subtract end - start
    dataframe['Difference'] = end - start
    #Set all differences that do not equal 0 to the dataframe and return it
    dataframe = dataframe[dataframe['Difference']!=pd.Timedelta(0)].dropna()
    return dataframe

def cleanZips(dataframe):
    dataframe['Zipcode'] = dataframe['Zipcode'].str[:5]
    return dataframe

def fullClean(dataframe):
    #Perform all clean functions on dataframe
    x = clean(dataframe)
    x = cleanIfMoreThanThreeNaN(x)
    x = cleanDistance(x)
    x = cleanZips(x)
    x = cleanTimes(x)
    return x

def q1(dataframe):
    #Return the mode of the month value of all the Start_Times
    return dataframe['Start_Time'].dt.month.mode().to_string(index=False)

def q2(dataframe):
    #Set all start times to time variable
    time = dataframe['Start_Time']
    #Set newrows variable to all start times if they are in 2020
    newrows = dataframe[(time.dt.year == 2020)]
    #Return the mode of the newrows dataframe's 'State' variable
    return newrows['State'].mode().to_string(index=False)

def q3(dataframe):
    #Set all start times to time variable
    time = dataframe['Start_Time']
    #Set all severities to sev variable
    sev = dataframe['Severity']
    #Set newrows variable to all rows that equal 2021 with a severity of 2
    newrows = dataframe[(time.dt.year == 2021) & (sev == 2)]
    #Return the mode of the states in the newrows dataframe
    return newrows['State'].mode().to_string(index=False)

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
    states = dataframe['State']
    #Set years to all years
    years = data['Start_Time'].dt.year
    #Loop through them both 
    for x, y in zip(years, states):
        if x == 2019 and y == 'CA':
            return cities.value_counts()[:5].index.tolist()

def q6(dataframe):
    #Get temp and humidity columns
    temp = dataframe.loc[dataframe['Severity'] == 4, 'Temperature(F)']
    hum = dataframe.loc[dataframe['Severity'] == 4, 'Humidity(%)']
    return "Temperature: {}   Humidity: {}".format(round(temp.mean(), 3), round(hum.mean(), 3))

def q7(dataframe):
    #Set all weather conditions to one variable
    weather = dataframe['Weather_Condition']
    #Return the 3 most common weather types
    return weather.value_counts()[:3].index.tolist()

def q8(dataframe):
    #Set all visibilities to one variable
    # such that the value for the rows 'State' column is equal to NH
    visibility = dataframe.loc[dataframe['State'] == 'NH', 'Visibility(mi)']
    #Return the max visibility of that new variable
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
    #Set all start times to one variable
    startTime = dataframe['Start_Time']
    #Set all states to one variable
    state = dataframe['State']
    #Set all of march to one variable
    march = dataframe[(startTime.dt.year == 2021) & (startTime.dt.month == 3) & (state == 'FL')]
    #Set all of april to one variable
    april = dataframe[(startTime.dt.year == 2021) & (startTime.dt.month == 4) & (state == 'FL')]
    #Set all of may to one variable
    may = dataframe[(startTime.dt.year == 2021) & (startTime.dt.month == 5) & (state == 'FL')]
    #Find the different in time for each month
    marchTime = march['End_Time'] - march['Start_Time']
    aprilTime = april['End_Time'] - april['Start_Time']
    mayTime = may['End_Time'] - may['Start_Time']
    #Find the largest different of each month
    maxMarchTime = marchTime.max()
    maxAprilTime = aprilTime.max()
    maxMayTime = mayTime.max()
    #Simple if statement to find the largest different between all 3 months
    if maxMarchTime > maxAprilTime and maxMarchTime > maxMayTime:
        return maxMarchTime
    elif maxAprilTime > maxMarchTime and maxAprilTime > maxMayTime:
        return maxAprilTime
    elif maxMayTime > maxMarchTime and maxMayTime > maxAprilTime:
        return maxMayTime

#Menu Start
def menu():
    print("\n(1) Load data")
    print("(2) Process data")
    print("(3) Print Answers")
    print("(4) Search Accidents (Use City, State, and Zip Code)")
    print("(5) Search Accidents (Year, Month and Day)")
    print("(6) Search Accidents (Temperature Range and Visibility Range)")
    print("(7) Quit")

while(True):
    start = time.time()
    def currTime():
        x = round(time.time()-start, 2)
        return x
    try:
        menu()
        option = int(input("\nEnter your option: "))
        print("Option", option, "has been selected")
        
        if option == 1:
            print("\nLoading and cleaning input data set:")
            print("************************************")
            print("Current time[{} seconds] Starting Script".format(currTime()))
            print("Current time[{} seconds] Loading US_Accidents_data.csv".format(currTime()))
            data = pd.read_csv('US_Accidents_data.csv')
            print("Current time[{} seconds] Total Columns Read: {}".format(currTime(), len(data.columns)))
            print("Current time[{} seconds] Total Rows Read: {}".format(currTime(), len(data)))
            print("Time to load is: {}".format(currTime()))
        
        elif option == 2:
            print("\nProcessing input data set:")
            print("************************************")
            print("Current time[{} seconds] Performing full data clean up".format(currTime()))
            data = fullClean(data)
            print("Current time[{} seconds] Row count after cleaning: {}".format(currTime(), len(data)), "\n")
            #print("Time to load is: ")
       
        elif option == 3:
            print("\nAnswering questions:")
            print("************************************")
           #Question 1
            print("Current time[{} seconds] (Q1) In what month were there more accidents reported? {}"
                .format(currTime(), q1(data)))
            #Question 2
            print("Current time[{} seconds] (Q2) What is the state that had the most accidents in 2020? {}"
                .format(currTime(), q2(data)))
            #Question 3
            print("Current time[{} seconds] (Q3) What is the state that had the most accidents of severity 2 in 2021? {}"
                .format(currTime(), q3(data)))
            #Question 4
            print("Current time[{} seconds] (Q4) What severity is the most common in Virginia? {}"
                .format(currTime(), q4(data)))    
            #Question 5
            print("Current time[{} seconds] (Q5) What are the 5 cities that had the most accidents in 2019 in California? {}"
                .format(currTime(), q5(data)))
            #Question 6
            print("Current time[{} seconds] (Q6) What was the average humidity and average temperature of all accidents of severity 4 that occurred in 2021? {}"
                .format(currTime(), q6(data)))
            #Question 7
            print("Current time[{} seconds] (Q7) What are the 3 most common weather conditions (weather_conditions) when accidents occurred? {}"
                .format(currTime(), q7(data)))
            #Question 8
            print("Current time[{} seconds] (Q8) What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire? {}"
                .format(currTime(), q8(data)))
            #Question 9
            print("Current time[{} seconds] (Q9) How many accidents of each severity were recorded in Bakersfield? {}"
                .format(currTime(), q9(data)))
            #Question 10
            print("Current time[{} seconds] (Q10) What was the longest accident (in hours) recorded in Florida in the Spring (March, April, and May) of 2022? {}"
                .format(currTime(), q10(data)))  
        
        elif option == 4:
            #Take 3 input variables, set answer to the dataframe entries where all 3 inputs are found
            c, s, z = input("\nSearch Accidents (Use City, State, and Zip Code):").split()
            answer = data[(data['City'] == c) & (data['State'] == s) & (data['Zipcode'] == z)]
            print("There were {} accidents found.".format(len(answer)))
            print("Time to perfom this search is: {}".format(currTime()))
            print("************************************")
        
        elif option == 5:
            #Take input (y), convert it to a datetime, print where the dataframe has equal datetimes as y
            x = data['Start_Time']
            y = input("\nSearch Accidents (Use Year, Month, and Day 2022-01-20):")
            y = pd.to_datetime(y)
            answer2 = data[(x.dt.year == y.year) & (x.dt.month == y.month) & (x.dt.day == y.day)]
            print("There were {} accidents found.".format(len(answer2)))
            print("Time to perfom this search is: {}".format(currTime()))
            print("************************************")
        
        elif option == 6:
            #Take 2 input variables, convert them to floats to match dataframe columns, print the rows with those variables
            temp, vis = input("\nSearch Accidents (Temperature and Visibility):").split()
            temp = float(temp)
            vis = float(vis)
            answer3 = data[(data['Temperature(F)'] == temp) & (data['Visibility(mi)'] == vis)]
            print("There were {} accidents found.".format(len(answer3)))
            print("Time to perfom this search is: {}".format(currTime()))
            print("************************************")        
        
        elif option == 7:
            print('\nTotal Running Time (In Minutes):{}'.format(currTime() / 60))
            exit()
        
        else:
            print("\nInvalid option, please try again.")
    
    except ValueError:
        print("\nInvalid option, please try again.")
        


