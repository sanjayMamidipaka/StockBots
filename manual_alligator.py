import pandas as pd
import tulipy as ti
import matplotlib.pyplot as plt
import numpy as np
import backtester

b = backtester.Backtester(1000)
numTrades = 0
initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial = initial[::-1].reset_index(drop=True)
green = ti.wilders(np.array(initial['open']), 5)
red = ti.wilders(np.array(initial['open']), 8)
blue = ti.wilders(np.array(initial['open']), 13)
rsi = ti.rsi(np.array(initial['open']), 26)
bband1 = ti.bbands(np.array(initial['open']), 200, 2)[0]
bband2 = ti.bbands(np.array(initial['open']), 200, 2)[2]
indicators = pd.concat([pd.DataFrame(green), pd.DataFrame(red), pd.DataFrame(blue), pd.DataFrame(rsi), pd.DataFrame(bband1), pd.DataFrame(bband2)], axis=1)
initial = pd.concat([initial, indicators], axis = 1)
initial.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'green', 'red', 'blue', 'rsi', 'bband1', 'bband2']
initial.green = initial.green.shift(periods=3, fill_value=0)
initial.red = initial.red.shift(periods=5, fill_value=0)
initial.blue = initial.blue.shift(periods=8, fill_value=0)
initial['close'].plot()


buyx = []
buyy = []
sellx = []
selly = []
for i in range(50,len(initial)-1):
    one = int(initial['green'][i] > initial['red'][i] and initial['red'][i] > initial['blue'][i])
    two = int(initial['rsi'][i] <= 30)
    three = int(initial['bband1'][i] - initial['open'][i] <= 0.01 or initial['open'][i] <= initial['bband1'][i])
    total = one + two + three 

    newOne = int(initial['open'][i] > initial['blue'][i] and initial['open'][i] > initial['red'][i] and initial['open'][i] > initial['green'][i])
    newTwo = int(initial['rsi'][i] >= 70)
    newThree = int(initial['open'][i] - initial['bband2'][i] <= 0.01 or initial['open'][i] >= initial['bband2'][i])
    newTotal = newOne + newTwo + newThree
    if (total >= 2):
        if b.buy(5, float(initial['open'][i]), i):
            buyx.append(i)
            buyy.append(initial['open'][i])
            numTrades += 1
    
    elif (newTotal >= 2):
        if b.sell(5, float(initial['open'][i]), i):
            sellx.append(i)
            selly.append(initial['open'][i])


if b.sell(5, b.get_current_buys(), i):
    sellx.append(i)
    selly.append(initial['open'][i])

plt.scatter(buyx, buyy, color='green')
plt.scatter(sellx, selly, color='red')
print(b.get_returns())
print('trade pairs:', numTrades)
plt.show()
