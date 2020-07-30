import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import backtester, math
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle
from sklearn.preprocessing import MinMaxScaler 
from keras.models import Sequential 
from keras.layers import Dense, LSTM 

initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial = initial[::-1].reset_index(drop=True)
#initial = initial[:500]
scaler = MinMaxScaler(feature_range=(0,1))
model = 1
buy_price = 0.0
initialInvestment = 1000
b = backtester.Backtester(initialInvestment)
predictions = []
with open('lstm.pkl', 'rb') as file:
    model = pickle.load(file)

scaler.fit(initial.filter(['close']))
for i in range(len(initial)-60):
    new_df = initial.filter(['close'])
    last_60_days = new_df[i:60+i].values
    last_60_days_scaled = scaler.transform(last_60_days)

    X_test = []
    X_test.append(last_60_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    pred_price = model.predict(X_test)
    pred_price = scaler.inverse_transform(pred_price)
    predictions.append(float(pred_price))

    if pred_price > initial['close'].iloc[i]:
        if b.buy(math.floor(initialInvestment/initial['close'].iloc[i]), initial['close'].iloc[i], initial['close'].index[i]):
            buy_price = initial['close'].iloc[i]

    elif initial['close'].iloc[i] - buy_price >= 0.45:
        if b.sell(b.get_current_buys(), initial['close'].iloc[i], initial['close'].index[i]):
            pass

    if (initial['close'].iloc[i] - buy_price <= -0.20): #sell
        if b.sell(b.get_current_buys(), initial['close'].iloc[i], initial['close'].index[i]):
            pass

i = len(initial['close'].index)-1
if b.sell(b.get_current_buys(), initial['close'].iloc[i], i): #sell everything once the day is done
    print('oh')

print('Profit:', b.get_returns())

x_axis = []
for i in range(len(predictions)):
    x_axis.append(i+60)
plt.plot(x_axis, predictions, label='Predicted')
plt.plot(initial['close'], label='Actual')
plt.legend()
plt.show()