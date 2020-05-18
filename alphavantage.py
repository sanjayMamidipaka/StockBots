import backtester
from stockstats import StockDataFrame
import pandas as pd
import matplotlib.pyplot as plt
import math, numpy as np
import requests

final = 0.0
url = 'https://cloud.iexapis.com/stable/stock/mgnx/chart/1d?token=pk_6aaddf59a63c4cd6b41c4685dd60114d&exactDate=20200512'
r = requests.get(url)
initial = pd.read_json(r.content)

stock = StockDataFrame.retype(initial)
initial['bband1'] = stock['boll_lb']
initial['bband2'] = stock['boll_ub']
initial['rsi'] = stock['rsi_6']
initialInvestment = 10000.0

sellx = []
selly = []
buyx = []
buyy = []
b = backtester.Backtester(initialInvestment)
stoploss = initial['close'][0] * 0.999
for i in range(0,len(initial.index)):

    if (stock['rsi_6'][i] < 30 and initial['close'][i] - initial['bband1'][i] < 0.1): #buy
        if b.buy(math.floor(initialInvestment/initial['close'][i]), initial['close'][i], i):
            buyx.append(initial['minute'][i])
            buyy.append(initial['close'][i])
            stoploss = initial['close'][i] * 0.999

    elif (stock['rsi_6'][i] > 70 and initial['bband2'][i] - initial['close'][i] < 0.1): #sell
        if b.sell(b.get_current_buys(), initial['close'][i], i):
            sellx.append(initial['minute'][i])
            selly.append(initial['close'][i])

    if initial['close'][i] <= stoploss: #stoploss
        if b.sell(b.get_current_buys(), initial['close'][i], i):
            sellx.append(initial['minute'][i])
            selly.append(initial['close'][i])

i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['close'][i], i): #sell evrything once the day is done
    sellx.append(initial['minute'][i])
    selly.append(initial['close'][i])


plt.plot(stock['minute'], initial['close'])
#initial[['close']].plot()

plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
final += float(b.get_returns())
plt.legend()
print(b.get_returns())
#plt.show()

print(final)
