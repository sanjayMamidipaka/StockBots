import backtester
from stockstats import StockDataFrame
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'msft', '1min','9YM6MWUWHMZN05MB', 'csv','full')

initial = pd.read_csv(r, index_col='timestamp', parse_dates=True)
initial = initial.iloc[::-1]
initial = initial[-350:]

stock = StockDataFrame.retype(initial)
initial['bband1'] = stock['boll_lb']
initial['bband2'] = stock['boll_ub']
initial['rsi'] = stock['rsi_6']
initialInvestment = 100000.0
initial.dropna()
b = backtester.Backtester(initialInvestment, initial)
sellx = []
selly = []
buyx = []
buyy = []

for i in range(0,len(initial.index)):
    if (stock['rsi_6'][i] < 30): #buy
        if b.buy(150, initial['close'][i], i):
            buyx.append(initial.index[i])
            buyy.append(initial['close'][i])

    elif (stock['rsi_6'][i] > 70): #sell
         if b.sell(b.get_current_buys(), initial['close'][i], i):
            sellx.append(initial.index[i])
            selly.append(initial['close'][i])

i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['close'][i], i):
    sellx.append(initial.index[i])
    selly.append(initial['close'][i])



initial.drop(['high', 'low', 'open', 'volume'], axis=1, inplace=True)
stock[['close']].plot()

plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
print(b.get_returns())
plt.legend()
plt.show()