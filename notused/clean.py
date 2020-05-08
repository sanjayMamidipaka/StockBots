import backtester
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import requests, csv

initialInvestment = 15000.0
sellx = []
selly = []

buyx = []
buyy = []

allx = []
ally = []

def bbands(initialInvestment):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
    r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'SNAP', '1min','9YM6MWUWHMZN05MB', 'csv','full')

    average = pd.read_csv(r, index_col='timestamp', parse_dates=True)


    url = 'https://www.alphavantage.co/query?function=BBANDS&series_type=close&nbdevup=3&nbdevdn=3'
    r = '{}&symbol={}&interval={}&time_period={}&apikey={}&datatype={}'.format(url, 'SNAP', 'daily','5','9YM6MWUWHMZN05MB', 'csv','full')

    bbands = pd.read_csv(r, index_col='time', parse_dates=True)

    average = average.iloc[::-1]
    bbands = bbands.iloc[::-1]

    bbands.drop('Real Middle Band', axis=1, inplace=True)

    bbands['Average'] = average['close']
    b = backtester.Backtester(initialInvestment, bbands)
    for i in range(0,len(bbands.index),10): 
        if (bbands['Real Upper Band'][i] - bbands['Average'][i] < 1): #sell
            boolean = b.sell(10, float(bbands['Average'][i]), i)
            
            if boolean:
                sellx.append(bbands.index[i])
                selly.append(bbands['Average'][i])

        if (bbands['Average'][i] - bbands['Real Lower Band'][i] < 1): #buy
            boolean = b.buy(10, float(bbands['Average'][i]), i)

            if boolean:
                buyx.append(bbands.index[i])
                buyy.append(bbands['Average'][i])

    b.sell((len(buyx) - len(sellx)), float(bbands['Average'][i]), len(bbands.index)-2) #dump
    allx.append(bbands.index[i])
    ally.append((bbands['Average'][len(bbands['Average'])-1]))
    print(b.get_returns())
    bbands.plot(figsize=(20,8))


def vwap(initialInvestment):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
    r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'SNAP', '1min','9YM6MWUWHMZN05MB', 'csv','full')

    intraday = pd.read_csv(r, index_col='timestamp', parse_dates=True)

    url = 'https://www.alphavantage.co/query?function=VWAP'
    r = '{}&symbol={}&interval={}&apikey={}&datatype={}'.format(url, 'SNAP', '1min','9YM6MWUWHMZN05MB', 'csv','full')

    vwap = pd.read_csv(r, index_col='time', parse_dates=True)


    vwap = vwap.iloc[::-1]
    intraday = intraday.iloc[::-1]


    vwap['Average'] = intraday['close']
    b = backtester.Backtester(initialInvestment, vwap)
    vwap.plot(figsize=(20,8))
    vwap = vwap[-60:]
    for i in range(0,len(vwap.index),3): 

        if (vwap['Average'][i] - vwap['VWAP'][i] < 0.01): #buy
            boolean = b.buy(1, float(vwap['Average'][i]), i)

            if boolean:
                buyx.append(vwap.index[i])
                buyy.append(vwap['Average'][i])

        elif (vwap['VWAP'][i] - vwap['Average'][i] < 0.01): #sell
            boolean = initialInvestment = b.sell(1, float(vwap['Average'][i]), i) # returns true if a trade was actually executed

            if boolean: # if a trade was executed, plot it
                sellx.append(vwap.index[i])
                selly.append(vwap['Average'][i])

    b.sell((len(buyx) - len(sellx)), float(vwap['Average'][i]), len(vwap.index)-2) #dump
    allx.append(vwap.index[i])
    ally.append((vwap['Average'][len(vwap['Average'])-1]))
    print(b.get_returns())

    

bbands(initialInvestment)
plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
plt.scatter(allx, ally,c='black', label='dump')
plt.legend()
plt.show()
