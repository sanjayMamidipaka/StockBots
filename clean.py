import backtester
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

initialInvestment = 10000.0
sellx = []
selly = []

buyx = []
buyy = []

def bbands(initialInvestment):
    bbands = pd.read_csv('bbands.csv', index_col='time', parse_dates=True)
    average = pd.read_csv('total.csv', index_col='timestamp', parse_dates=True)

    average = average.iloc[::-1]
    bbands = bbands.iloc[::-1]


    bbands.drop('Real Middle Band', axis=1, inplace=True)

    bbands['Average'] = average['close']
    b = backtester.Backtester(initialInvestment, bbands)
    for i in range(len(bbands.index)): 
        if (bbands['Real Upper Band'][i] - bbands['Average'][i] < 2): #sell
            b.sell(10, float(bbands['Average'][i]), i)
            sellx.append(bbands.index[i])
            selly.append(bbands['Average'][i])

        if (bbands['Average'][i] - bbands['Real Lower Band'][i] < 2): #buy
            b.buy(10, float(bbands['Average'][i]), i)
            buyx.append(bbands.index[i])
            buyy.append(bbands['Average'][i])

    print(b.get_returns())
    bbands.plot()


def vwap(initialInvestment):
    vwap = pd.read_csv('vwap.csv', index_col='time', parse_dates=True)
    intraday = pd.read_csv('intraday.csv', index_col='timestamp', parse_dates=True)

    vwap = vwap.iloc[::-1]
    intraday = intraday.iloc[::-1]

    vwap = vwap[-1000:]
    intraday = intraday[-1000:]

    vwap['Average'] = intraday['close']
    b = backtester.Backtester(initialInvestment, vwap)
    vwap.plot(figsize=(20,4))
    for i in range(0,len(vwap.index),3): 
        if (vwap['vwap'][i] - vwap['Average'][i] < 0.1): #sell
            initialInvestment = b.sell(10, float(vwap['Average'][i]), i)
            sellx.append(vwap.index[i])
            selly.append(vwap['Average'][i])

        elif (vwap['Average'][i] - vwap['vwap'][i] < 0.1): #buy
            initialInvestment = b.buy(10, float(vwap['Average'][i]), i)
            buyx.append(vwap.index[i])
            buyy.append(vwap['Average'][i])

    print(b.get_returns())

    

vwap(initialInvestment)
plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
plt.legend()
plt.show()
