import backtester
from stockstats import StockDataFrame
import pandas as pd
import matplotlib.pyplot as plt
import math, numpy as np
import tulipy as ti

final = 0.0
#initial = pd.read_csv('https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1577836800&period2=1590105600&interval=1d&events=history')
initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=msft&interval=1min&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
bband1 = ti.bbands(np.array(initial['open']), 26, 2)[0]
bband2 = ti.bbands(np.array(initial['open']), 26, 2)[2]
rsi_26 = ti.rsi(np.array(initial['open']),26)
bbands = pd.concat([pd.DataFrame(bband1),pd.DataFrame(bband2),pd.DataFrame(rsi_26)], axis=1)
initial = pd.concat([initial, bbands], axis = 1)
initial = initial.iloc[::-1]
initial.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'bband1', 'bband2', 'rsi']


initialInvestment = 1000.0
stopprofit = float(initial['open'][0]) * (1+0.01)
stoploss = float(initial['open'][0]) * (1-0.01)

b = backtester.Backtester(initialInvestment)
for i in range(200,len(initial.index)):
    one = int(initial['open'].ewm(span=50).mean()[i] > initial['open'].ewm(span=200).mean()[i]) #ema
    two = int(initial['rsi'][i] <= 30) # rsi
    three = int(initial['open'][i] - initial['bband1'][i] <= 0.01) #bollinger bands
    total = one + two + three

    newOne = int(initial['open'].ewm(span=50).mean()[i] < initial['open'].ewm(span=200).mean()[i])
    newTwo = int(initial['rsi'][i] >= 70)
    newThree = int(initial['bband1'][i] - initial['open'][i] <= 0.01)
    newTotal = newOne + newTwo + newThree

    

    if (total >= 2): #buy
        if b.buy(math.floor(float(initialInvestment)/float(initial['open'][i])), float(initial['open'][i]), i):
            pass

    elif (newTotal >= 2 or initial['open'][i] <= stoploss or initial['open'][i] >= stopprofit): #sell
        if b.sell(b.get_current_buys(), initial['close'][i], i):
            pass

    stopprofit = float(initial['open'][i-1]) * (1+0.01)
    stoploss = float(initial['open'][i-1]) * (1-0.01)



i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['close'][i], i): #sell everything once the day is done
    print('sell')



#plt.scatter(sellx, selly,c='red', label='sell')
#plt.scatter(buyx, buyy,c='green', label='buy')
#plt.legend()
print(b.get_returns())
#plt.show()
