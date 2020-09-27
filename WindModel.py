import json
import urllib.request, urllib.parse, urllib.error 
import pandas as pd
import numpy as np
import pickle
from sklearn import metrics
from sklearn import linear_model 
from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
import math
import datetime



data = pd.read_csv('wind_generation_data.csv', sep=",")

# Defining features for the modelling
X = data.drop(['Power Output'], axis = 1).values 
y = data['Power Output'].values 

# Create training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Fit training sets in the model
lm = linear_model.LinearRegression()
lm.fit(X_train,y_train)


### Using the Model on the dataset from the open weather api

# Load weather data from Openweather API using the urllib library 
json_string = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/onecall?lat=53.556563&lon=8.598084&exclude=hourly,minutely&appid=d51a4ce07859ab07bfd361e1c455940e').read()
WindWeather = json.loads(json_string)

# Convert the loaded data to a dataframe and choose the daily weather conditions
data = pd.DataFrame(WindWeather['daily'])

# Dropping all columns not needed to fit in model
df1 = data.drop(['sunrise','sunset','pressure','humidity','dew_point', 'clouds','uvi','pop','rain','sunrise','sunset','feels_like','weather','temp'], axis = 1)

# Renaming the column as per the model fitting dataframe
df1= df1.rename(columns = {'dt': 'Date','wind_deg': 'direction', 'wind_speed': 'wind speed'}, inplace = False)

# Converting the Epoch time to normal time
df1["Date"] = pd.to_datetime(df1["Date"],unit = 's')

# Creating a Day column from Date for the maintanence schedule logic
df1["Day"] = df1["Date"].dt.day

# Drop the date and day column for predicting Power Output
data2 = df1.drop(['Date','Day'], axis = 1)

# Define X inputs to fit and predict 
X1 = data2.values

# Predicting power output
y = lm.predict(X1)

# Convert the predicted power output from an array into a dataframe
PowerOutput_Wind = pd.DataFrame(y)

# Append the predicted power output to df1.
df1['PowerOutput_Wind'] = PowerOutput_Wind

# Display the expected power output for 4 consecutive days
df1 = df1[0:5]
#print(df1) #for prediction display

# Logic for maintenance schedule according to the maintenance csv days
df1['PowerOutput_Wind'] = np.select([df1.Day == 3, df1.Day == 5,df1.Day == 7,df1.Day == 8,df1.Day == 15,df1.Day == 24,df1.Day == 28], 
			[0.7*df1.PowerOutput_Wind,0.6*df1.PowerOutput_Wind, 0.5*df1.PowerOutput_Wind,0.45*df1.PowerOutput_Wind,0.55*df1.PowerOutput_Wind,
			0.9*df1.PowerOutput_Wind,0.3*df1.PowerOutput_Wind ], default=df1.PowerOutput_Wind)

#print(df1) #for prediction display

#Save model as a Pickle file
pickle.dump(lm,open('modelWind.pkl','wb'))
model= pickle.load(open('modelWind.pkl','rb'))





