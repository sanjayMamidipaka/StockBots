import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import pandas_ta as ta
import backtester, math
import seaborn as sns
from scipy.signal import find_peaks, find_peaks_cwt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle
sns.set()

initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial = initial[::-1].reset_index(drop=True)
volume = initial['volume']
initial.drop(['volume', 'timestamp'], axis=1, inplace=True)
bbands = ta.bbands(initial['close'], length=50, std=2) #calculating indicators
rsi = ta.rsi(initial['close'], length=20)
ema_50 = ta.ema(initial['close'], length=5)
ema_200 = ta.ema(initial['close'], length=20)
ema_500 = ta.ema(initial['close'], length=50)
#macd = ta.macd(initial['close'], 5, 35, 5)
vwap = ta.vwap(initial['high'], initial['low'], initial['close'], volume)
initial = pd.concat([initial, bbands, ema_50, ema_200, ema_500, vwap], axis=1)

initial.columns =['open', 'high', 'low', 'close', 'bband1', 'useless', 'bband2', 'ema1', 'ema2', 'ema3', 'vwap']
initialInvestment = 1000
b = backtester.Backtester(initialInvestment)
initial = initial.dropna()
X = initial.drop('close', axis=1)
y = initial['close']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle = False, stratify = None)
from sklearn.ensemble import RandomForestRegressor
rfc = RandomForestRegressor(n_estimators=100)
rfc.fit(X_train, y_train)

buyx = []
buyy = []
sellx = []
selly = []
predictions = [y_test.iloc[-1]]
for i in range(len(X_test)):
    pred = rfc.predict([X_test.iloc[i]])
    
    if pred[0] > float(predictions[-1]):
        if b.buy(math.floor(initialInvestment/y_test.iloc[i]), y_test.iloc[i], y_test.index[i]):
            buyx.append(y_test.index[i])
            buyy.append(y_test.iloc[i])

    elif pred[0] < float(predictions[-1]):
        if b.sell(b.get_current_buys(), y_test.iloc[i], y_test.index[i]):
            sellx.append(y_test.index[i])
            selly.append(y_test.iloc[i])

    predictions.append(pred)

i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['close'].iloc[i], i): #sell everything once the day is done
    print('oh')
    sellx.append(initial.index[i])
    selly.append(initial['open'].iloc[i])

print('Profit:', b.get_returns())

s = input('Would you like to save?\n')
if s == 'yes':
    pkl_filename = "stock_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(rfc, file)

#plt.show()