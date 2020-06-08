import backtester
import pandas as pd
import matplotlib.pyplot as plt
import math, numpy as np
import tulipy as ti
import seaborn as sns

final = 0.0
numTrades = 0
initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
bband1 = ti.bbands(np.array(initial['open']), 50, 2)[0]
bband2 = ti.bbands(np.array(initial['open']), 50, 2)[2]
rsi_26 = ti.rsi(np.array(initial['open']), 14)
ema_50 = ti.ema(np.array(initial['open']), 50)
ema_200 = ti.ema(np.array(initial['open']), 200)
bbands = pd.concat([pd.DataFrame(bband1),pd.DataFrame(bband2),pd.DataFrame(rsi_26), pd.DataFrame(ema_50), pd.DataFrame(ema_200)], axis=1)
initial = pd.concat([initial, bbands], axis = 1)
initial.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'bband1', 'bband2', 'rsi', 'ema1', 'ema2']
initial.drop(['high','low','close','volume'], axis=1, inplace=True)
sellx = []
selly = []
buyx = []
buyy = []

initialInvestment = 1000.0

b = backtester.Backtester(initialInvestment)
for i in range(len(initial.index)-200,1,-1):
    one = int(initial['ema1'][i] >= initial['ema2'][i]) #ema
    two = int(initial['rsi'][i] <= 30) # rsi
    three = int(initial['bband1'][i] - initial['open'][i] <= 0.01 or initial['open'][i] <= initial['bband1'][i]) #bollinger bands
    total = one + two + three

    newOne = int(initial['ema1'][i] <= initial['ema2'][i])
    newTwo = int(initial['rsi'][i] >= 70)
    newThree = int(initial['open'][i] - initial['bband2'][i] <= 0.01 or initial['open'][i] >= initial['bband2'][i])
    newTotal = newOne + newTwo + newThree

    

    if (total >= 2): #buy
        if b.buy(math.floor(float(initialInvestment)/float(initial['open'][i])), float(initial['open'][i]), i):
            numTrades += 1
            buyx.append(i)
            buyy.append(initial['open'][i])

    elif (newTotal >= 2): #sell
        if b.sell(b.get_current_buys(), initial['open'][i], i):
            sellx.append(i)
            selly.append(initial['open'][i])

    



i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['open'][i], i): #sell everything once the day is done
    sellx.append(i)
    selly.append(initial['open'][i])



initial['open'].plot()
plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
plt.legend()
print(b.get_returns())
print('Number of buy-sell pairs:', numTrades)
plt.show()
