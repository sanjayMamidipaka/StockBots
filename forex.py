#OANDA Key: 6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85
#account id thing: 101-001-15560575-001
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np , requests
import pandas_ta as ta
import backtester, math
from datetime import datetime, timedelta
import seaborn as sns
sns.set()

initial = pd.read_csv('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=eur&to_symbol=USD&interval=1min&apikey=OUMVBY0VK0HS8I9E&outputsize=full&datatype=csv', index_col='timestamp', parse_dates=True)
initial = initial[::-1]
#initial = initial[initial.index > '2020-07-05 09:30:00']

bbands = ta.bbands(initial['close'], length=200, std=2) #calculating indicators
ema_5 = ta.ema(initial['close'], length=50)
ema_20 = ta.ema(initial['close'], length=200)
ema_50 = ta.ema(initial['close'], length=500)
macd = ta.macd(initial['close'], 5, 35, 5)
rsi = ta.rsi(initial['close'], 50)
initial = pd.concat([initial, bbands, ema_5, ema_20, ema_50, macd, rsi], axis=1)
initial.columns =['open', 'high', 'low', 'close', 'bband1', 'useless', 'bband2', 'ema1', 'ema2', 'ema3', 'macd', 'macdh', 'macds', 'rsi']

initialInvestment = 1000
numTrades = 0
buyx = []
buyy = []
sellx = []
selly = []
b = backtester.Backtester(initialInvestment)
for i in range(50,len(initial.index)-1):
    one = int(initial['ema1'][i] >= initial['ema2'][i] and initial['ema2'][i] >= initial['ema3'][i]) #hma, hull moving average
    two = int(initial['macd'][i] >= initial['macds'][i] and initial['macdh'][i] >= 0) # macd
    three = int(initial['bband1'][i] - initial['open'][i] <= 0.01 or initial['open'][i] <= initial['bband1'][i]) #bollinger bands
    four = int(initial['rsi'][i] <= 30)
    total = one + two + three + four

    newOne = int(initial['ema1'][i] < initial['ema2'][i] and initial['ema2'][i] < initial['ema3'][i])
    newTwo = int(initial['macd'][i] < initial['macds'][i] and initial['macdh'][i] < 0)
    newThree = int(initial['open'][i] - initial['bband2'][i] <= 0.01 or initial['open'][i] >= initial['bband2'][i])
    newFour = int(initial['rsi'][i] >= 70)
    newTotal = newOne + newTwo + newThree + newFour

    if (total >= 3): #buy
        if b.buy(math.floor(initialInvestment/initial['open'][i]), float(initial['open'][i]), initial.index[i]):
            numTrades += 1
            buyx.append(initial.index[i])
            buyy.append(initial['open'][i])

    elif (newTotal >= 3): #sell
        if b.sell(b.get_current_buys(), initial['open'][i], initial.index[i]):
            sellx.append(initial.index[i])
            selly.append(initial['open'][i])


i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['open'][i], i): #sell everything once the day is done
    sellx.append(initial.index[i])
    selly.append(initial['open'][i])

initial['close'].plot()
plt.scatter(sellx, selly,c='red', label='sell', marker='^')
plt.scatter(buyx, buyy,c='green', label='buy', marker='^')
plt.legend()
print(b.get_returns())
print('Number of buy-sell pairs:', numTrades)
print('Sharpe ratio:', b.get_sharpe())
plt.show()
