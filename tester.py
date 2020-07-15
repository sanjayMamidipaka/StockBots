import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import pandas_ta as ta
import backtester, math
import seaborn as sns
sns.set()

initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full', index_col='timestamp', parse_dates=True)
initial = initial[::-1]
#initial = initial[initial.index >= '2020-07-02 09:30:00']

bbands = ta.bbands(initial['close'], length=50, std=2) #calculating indicators
rsi = ta.rsi(initial['close'], )
ema_50 = ta.ema(initial['close'], length=5)
ema_200 = ta.ema(initial['close'], length=20)
macd = ta.macd(initial['close'], 12, 26, 9)
vwap = ta.vwap(initial['high'], initial['low'], initial['close'], initial['volume'])
initial = pd.concat([initial, bbands, ema_50, ema_200, macd, vwap], axis=1)
initial.columns =['open', 'high', 'low', 'close', 'volume', 'bband1', 'useless', 'bband2', 'ema1', 'ema2', 'macd', 'macdh', 'macds', 'vwap']

initialInvestment = 1000
numTrades = 0
buyx = []
buyy = []
sellx = []
selly = []
b = backtester.Backtester(initialInvestment)
for i in range(50,len(initial.index)-1):
    one = int(initial['ema1'][i] >= initial['ema2'][i]) #hma, hull moving average
    two = int(initial['macd'][i] >= initial['macds'][i] and initial['macdh'][i] >= 0) # macd
    three = int(initial['bband1'][i] - initial['open'][i] <= 0.01 or initial['open'][i] <= initial['bband1'][i]) #bollinger bands
    four = int(initial['open'][i] <= initial['vwap'][i]) #vwap
    total = one + two + three + four

    newOne = int(initial['ema1'][i] < initial['ema2'][i])
    newTwo = int(initial['macd'][i] < initial['macds'][i] and initial['macdh'][i] < 0)
    newThree = int(initial['open'][i] - initial['bband2'][i] <= 0.01 or initial['open'][i] >= initial['bband2'][i])
    newFour = int(initial['open'][i] > initial['vwap'][i]) #vwap
    newTotal = newOne + newTwo + newThree + newFour
    print(initial.tail())

    

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

initial['open'].plot()
plt.scatter(sellx, selly,c='red', label='sell', marker='^')
plt.scatter(buyx, buyy,c='green', label='buy', marker='^')
plt.legend()
print(b.get_returns())
print('Number of buy-sell pairs:', numTrades)
print('Sharpe ratio:', b.get_sharpe())
plt.show()
