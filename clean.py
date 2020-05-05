import backtester
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import requests, csv

initialInvestment = 1000.0
sellx = []
selly = []

buyx = []
buyy = []

def bbands(initialInvestment):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
    r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'MSFT', '1min','9YM6MWUWHMZN05MB', 'csv','full')

    average = pd.read_csv(r, index_col='timestamp', parse_dates=True)

    url = 'https://www.alphavantage.co/query?function=BBANDS&series_type=close&nbdevup=3&nbdevdn=3'
    r = '{}&symbol={}&interval={}&time_period={}&apikey={}&datatype={}'.format(url, 'MSFT', 'daily','5','9YM6MWUWHMZN05MB', 'csv','full')

    bbands = pd.read_csv(r, index_col='time', parse_dates=True)

    average = average.iloc[::-1]
    bbands = bbands.iloc[::-1]

    average = average[-1000:]
    bbands = bbands[-1000:]

    bbands.drop('Real Middle Band', axis=1, inplace=True)

    bbands['Average'] = average['close']
    b = backtester.Backtester(initialInvestment, bbands)
    for i in range(0,len(bbands.index)): 
        if (bbands['Real Upper Band'][i] - bbands['Average'][i] < 2): #sell
            boolean = b.sell(1, float(bbands['Average'][i]), i)
            
            if boolean:
                sellx.append(bbands.index[i])
                selly.append(bbands['Average'][i])

        if (bbands['Average'][i] - bbands['Real Lower Band'][i] < 2): #buy
            boolean = b.buy(1, float(bbands['Average'][i]), i)

            if boolean:
                buyx.append(bbands.index[i])
                buyy.append(bbands['Average'][i])

    print(b.get_returns())
    bbands.plot(figsize=(20,12))


def vwap(initialInvestment):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
    r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'MSFT', '1min','9YM6MWUWHMZN05MB', 'csv','full')

    intraday = pd.read_csv(r, index_col='timestamp', parse_dates=True)

    url = 'https://www.alphavantage.co/query?function=VWAP'
    r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'MSFT', '1min','9YM6MWUWHMZN05MB', 'csv','full')

    vwap = pd.read_csv('vwap.csv', index_col='time', parse_dates=True)


    vwap = vwap.iloc[::-1]
    intraday = intraday.iloc[::-1]


    vwap['Average'] = intraday['close']
    b = backtester.Backtester(initialInvestment, vwap)
    vwap.plot(figsize=(20,12))
    for i in range(0,len(vwap.index)): 
        if (vwap['vwap'][i] - vwap['Average'][i] < 2): #sell
            boolean = initialInvestment = b.sell(2, float(vwap['Average'][i]), i) # returns true if atrade was actually executed

            if boolean: # if a trade was executed, plot it
                sellx.append(vwap.index[i])
                selly.append(vwap['Average'][i])

        elif (vwap['Average'][i] - vwap['vwap'][i] < 2): #buy
            boolean = b.buy(2, float(vwap['Average'][i]), i)

            if boolean:
                buyx.append(vwap.index[i])
                buyy.append(vwap['Average'][i])

    print(b.get_returns())

    

bbands(initialInvestment)
plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
plt.legend()
plt.show()
