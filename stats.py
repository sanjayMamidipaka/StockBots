import backtester
from stockstats import StockDataFrame
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'msft', '1day','9YM6MWUWHMZN05MB', 'csv','full')

initial = pd.read_csv(r, index_col='timestamp', parse_dates=True)
initial = initial.iloc[::-1]

stock = StockDataFrame.retype(pd.read_csv(r, index_col='timestamp', parse_dates=True).iloc[::-1])
initial['bband1'] = stock['boll_lb']
initial['bband2'] = stock['boll_ub']
initialInvestment = 10000.0
initial.dropna()
b = backtester.Backtester(initialInvestment, initial)
sellx = []
selly = []
buyx = []
buyy = []
allx = []
ally = []
daterange = []

for i in range(0,len(initial.index)):
    if stock['adx'][i] > 25 and (stock['pdi'][i] > stock['mdi'][i]): #uptrend
        if b.buy(10, initial['close'][i], i):
            buyx.append(initial.index[i])
            buyy.append(initial['close'][i])
        daterange.append(initial.index[i])

    elif stock['adx'][i] > 25 and (stock['pdi'][i] < stock['mdi'][i]): #downtrend
         if b.sell(b.get_current_buys(), initial['close'][i], i):
            sellx.append(initial.index[i])
            selly.append(initial['close'][i])


boolean = b.sell(b.get_current_buys(), float(initial['close'][i]), i) #dump 
if boolean:
    allx.append(initial.index[i])
    ally.append(initial['close'][i])


initial.drop(['high', 'low', 'open', 'volume'], axis=1, inplace=True)
initial.plot()

plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
plt.scatter(allx, ally,c='black', label='dump')
print(b.get_returns())
plt.legend()
plt.show()