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

def get_decisions(close_column, distance):
    first = 0
    last = 20
    valleys = []
    peaks = []
    closes = close_column
    while last < len(initial.index):
        index = initial.index[first:last]
        temp = closes[first:last]
        valleys.append(index[np.argmin(temp)])
        peaks.append(index[np.argmax(temp)])
        first = first + distance
        last = last + distance


    decisions = [(np.nan) for i in range(len(initial.index))]
    for i in range(len(valleys)):
        decisions[valleys[i]] = 0

    for i in range(len(peaks)):
        decisions[peaks[i]] = 1

    return decisions

initial = pd.read_csv('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=aud&to_symbol=USD&interval=30min&apikey=OUMVBY0VK0HS8I9E&outputsize=full&datatype=csv')
initial = initial[::-1].reset_index(drop=True)
initial.drop('timestamp', axis=1, inplace=True)
bbands = ta.bbands(initial['close'], length=50, std=2) #calculating indicators
rsi = ta.rsi(initial['close'], length=14)
ema_50 = ta.ema(initial['close'], length=5)
ema_200 = ta.ema(initial['close'], length=20)
ema_500 = ta.ema(initial['close'], length=50)
macd = ta.macd(initial['close'], 5, 35, 5)
initial = pd.concat([initial, bbands, ema_50, ema_200, ema_500, macd, rsi], axis=1)
initial.columns =['open', 'high', 'low', 'close', 'bband1', 'useless', 'bband2', 'ema1', 'ema2', 'ema3', 'macd', 'macdh', 'macds', 'rsi']
initial['decisions'] = get_decisions(initial['close'], 50)

initialInvestment = 1000
b = backtester.Backtester(initialInvestment)
initial = initial.dropna()
numTrades = 0

X = initial.drop('decisions', axis=1)
y = initial['decisions']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle = False, stratify = None)
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train, y_train)

buyx = []
buyy = []
sellx = []
selly = []
predictions = []
for i in range(len(X_test)):
    pred = rfc.predict([X_test.iloc[i]])
    predictions.append(pred)

    if pred == 0:
        if b.buy(math.floor(initialInvestment/X_test['close'].iloc[i]), X_test['close'].iloc[i], X_test.index[i]):
            numTrades += 1
            buyx.append(X_test.index[i])

    elif pred == 1:
        if b.sell(b.get_current_buys(), X_test['close'].iloc[i], X_test.index[i]):
            sellx.append(X_test.index[i])
            selly.append(X_test['close'].iloc[i])

i = len(X_test.index)-1
if b.sell(b.get_current_buys(), X_test['close'].iloc[i], i): #sell everything once the day is done
    sellx.append(X_test.index[i])
    selly.append(X_test['close'].iloc[i])

print(b.get_returns())
print('Number of buy-sell pairs:', numTrades)
print('Sharpe ratio:', b.get_sharpe())

s = input('Would you like to save?\n')
if s == 'yes':
    pkl_filename = "forex_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(rfc, file)

plt.show()