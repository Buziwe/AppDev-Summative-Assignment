import json
import urllib.request, urllib.parse, urllib.error 
import pandas as pd
import pandas as pd
import numpy as np
import pickle
from sklearn import metrics
from sklearn import linear_model # for linear regression modeling
from sklearn import preprocessing # for preprocessing like imputting missing values
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
import math

data = pd.read_csv('solar_generation_data.csv', sep=",")

# Removing the degree sign from the temperature
data['Temp Hi'] = data['Temp Hi'].replace('°','', regex=True)
data['Temp Low'] = data['Temp Low'].replace('°','', regex=True)

# Replacing missing values with median
data.fillna(data.median(), inplace=True)

# Converting temp to float
data['Temp Hi'] = data['Temp Hi'].astype(float)
data['Temp Low'] = data['Temp Low'].astype(float)

# Defining features for the modelling
X = data.drop(['Power Generated in MW', 'Month ', 'Day','Rainfall in mm'], axis = 1).values 
y = data['Power Generated in MW'].values 

# Create training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Fit training sets in the model
lm = linear_model.LinearRegression()
model = lm.fit(X_train,y_train)


### Using the Model on the dataset from the open weather api

# Load weather data from Openweather API using the urllib library to convert into a dictionary
json_string = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/onecall?lat=-20.432510&lon=142.279680&exclude=hourly,minutely&appid=d51a4ce07859ab07bfd361e1c455940e').read()
SolarWeather = json.loads(json_string)

# Convert the loaded data to a dataframe and choose the daily weather conditions
data = pd.DataFrame(SolarWeather['daily'])


# Split temp dict into columns min and max temperature
data1= pd.DataFrame(data['temp'].values.tolist(), index=data.index)

# Dropping all columns not needed to fit in model
data2 = data.drop(['sunrise','sunset','pressure','humidity','dew_point', 'wind_speed','wind_deg','pop','sunrise','sunset','feels_like','weather','temp'], axis = 1)

# Merge the min and max temp columns onto the dataframe.
data2['Temp Low'] = data1['min']
data2['Temp Hi'] = data1['max']

# Replacing missing values with median
data2.fillna(data2.median(), inplace=True)

# Rename the columns to the same names as the model requires
df2 = data2.rename(columns = {'dt': 'Date','clouds': 'Cloud Cover Percentage', 'uvi': 'Solar'}, inplace = False)

# Convert from Epoch time to normal time
df2["Date"] = pd.to_datetime(df2["Date"],unit = 's')

# Creating a Day column from Date for the maintanence schedule logic
df2["Day"] = df2["Date"].dt.day

# Drop the date and day column for predicting Power Output
df3 = df2.drop(['Date','Day'], axis = 1)

# Define X inputs to fit and predict 
X1 = df3.values

# Predicting power output
y = lm.predict(X1)

# Convert the predicted power output from an array into a dataframe
PowerOutput_Solar = pd.DataFrame(y)

# Append the predicted power output to df2.
df2['PowerOutput_Solar'] = PowerOutput_Solar

# Display the expected power output for 4 consecutive days
df2 = df2[0:5]
#print(df2) #for prediction display

# Logic for maintenance schedule according to the maintenance csv days
df2['PowerOutput_Solar'] = np.select([df2.Day == 4, df2.Day == 6,df2.Day == 19,df2.Day == 23,df2.Day == 24,df2.Day == 25,df2.Day == 28], 
			[0.03*df2.PowerOutput_Solar,0.05*df2.PowerOutput_Solar, 0.02*df2.PowerOutput_Solar,0.5*df2.PowerOutput_Solar,0.2*df2.PowerOutput_Solar,
			0.05*df2.PowerOutput_Solar,0.1*df2.PowerOutput_Solar ], default=df2.PowerOutput_Solar)
#print(df2) #for prediction display

#Save model as a Pickle file
pickle.dump(lm,open('modelSolar.pkl','wb'))
model= pickle.load(open('modelSolar.pkl','rb'))



