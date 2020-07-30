import math
import numpy as np
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler 
from keras.models import Sequential 
from keras.layers import Dense, LSTM 
import matplotlib.pyplot as plt
import pickle
plt.style.use('fivethirtyeight')

df = pd.read_csv('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=aud&to_symbol=USD&interval=1min&apikey=OUMVBY0VK0HS8I9E&outputsize=full&datatype=csv')
data = df.filter(['close']) #only close colums
dataset = data.values #dataframe to numpy array
training_data_len = math.ceil(len(dataset) * 0.8) #training data length

#Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

#Create training set
#Create scaled set
train_data = scaled_data[0:training_data_len, : ]
#Split data into X_train, y_train
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])


#Convert to x_train and y_train numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train) 

#Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

#Build LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

#Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

#Train the model
model.fit(x_train, y_train, batch_size=1, epochs=2)

#Testing
test_data = scaled_data[training_data_len - 60: , :]
#Create the data setsx_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

#convert data to numpy array
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))


#Do inverse transformations
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#RMSE
rmse=np.sqrt(np.mean(((predictions- y_test)**2)))

#plot data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

#Visualize
plt.plot(train['close'])
plt.plot(valid[['close', 'Predictions']])
plt.show()

s = input('Would you like to save?\n')
if s == 'yes':
    pkl_filename = "forex_lstm.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

