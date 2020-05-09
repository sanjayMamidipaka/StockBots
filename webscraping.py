import backtester
from stockstats import StockDataFrame
import pandas as pd
import matplotlib.pyplot as plt
import math, bs4
import requests, csv 
from bs4 import BeautifulSoup
from web_scraper import scrape



# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
# r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'msft', '1min','9YM6MWUWHMZN05MB', 'csv','full')

# initial = pd.read_csv(r, index_col='timestamp', parse_dates=True)
# initial = initial.iloc[::-1]
# initial = initial[-350:]

rowlist = []
init = 0
final = 10
while init < final:
    rowlist.append(scrape())

    initial = pd.DataFrame(rowlist)

    stock = StockDataFrame.retype(initial)
    initial['bband1'] = stock['boll_lb']
    initial['bband2'] = stock['boll_ub']
    initial['rsi'] = stock['rsi_6']
    initialInvestment = 10000.0

    sellx = []
    selly = []
    buyx = []
    buyy = []
    b = backtester.Backtester(initialInvestment, initial)
    for i in range(0,len(initial.index)):
        if (stock['rsi_6'][i] < 30 and initial['close'][i] - initial['bband1'][i] < 0.5): #buy
            if b.buy(math.floor(initialInvestment/initial['close'][i]), initial['close'][i], i):
                buyx.append(initial.index[i])
                buyy.append(initial['close'][i])

        elif (stock['rsi_6'][i] > 70 and  initial['bband2'][i]-initial['close'][i] < 0.5): #sell
            if b.sell(b.get_current_buys(), initial['close'][i], i):
                sellx.append(initial.index[i])
                selly.append(initial['close'][i])

    i = len(initial.index)-1
    if b.sell(b.get_current_buys(), initial['close'][i], i):
        sellx.append(initial.index[i])
        selly.append(initial['close'][i])
    init += 1



#initial.drop(['high', 'low', 'open', 'volume'], axis=1, inplace=True)
# stock[['close']].plot()

# plt.scatter(sellx, selly,c='red', label='sell')
# plt.scatter(buyx, buyy,c='green', label='buy')
print(b.get_returns())
print(pd.DataFrame(rowlist))
# plt.legend()
# plt.show()