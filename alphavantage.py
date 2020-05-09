import backtester
from stockstats import StockDataFrame
import pandas as pd
import matplotlib.pyplot as plt
import math
import requests

final = 0.0

for j in range(29,32):
    try:
        url = 'https://cloud.iexapis.com/stable/stock/msft/chart/1d?token=pk_7f3367d0b5ee485bbac5d076f3511efd&exactDate=201912{}'.format(j)
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
        b = backtester.Backtester(initialInvestment, initial)
        for i in range(0,len(initial.index)):
            if (stock['rsi_6'][i] < 30 and initial['close'][i] - initial['bband1'][i] < 0.1): #buy
                if b.buy(math.floor(initialInvestment/initial['close'][i]), initial['close'][i], i):
                    buyx.append(initial['minute'][i])
                    buyy.append(initial['close'][i])

            elif (stock['rsi_6'][i] > 70 and initial['bband2'][i]-initial['close'][i] < 0.1): #sell
                if b.sell(b.get_current_buys(), initial['close'][i], i):
                    sellx.append(initial['minute'][i])
                    selly.append(initial['close'][i])

        i = len(initial.index)-1
        if b.sell(b.get_current_buys(), initial['close'][i], i):
            sellx.append(initial['minute'][i])
            selly.append(initial['close'][i])


        plt.plot(stock['minute'], initial['close'])
        #initial[['close']].plot()

        plt.scatter(sellx, selly,c='red', label='sell')
        plt.scatter(buyx, buyy,c='green', label='buy')
        final += float(b.get_returns())
        plt.legend()
        print(j, b.get_returns())
        #plt.show()

    except:
        print(1)

print(final)
