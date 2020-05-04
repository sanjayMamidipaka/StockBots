import backtester
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

initialInvestment = 10000.0
b = backtester.Backtester(initialInvestment) 
def bbands():
    bbands = pd.read_csv('bbands.csv', index_col='time', parse_dates=True)
    average = pd.read_csv('total.csv', index_col='timestamp', parse_dates=True)

    average = average.iloc[::-1]
    bbands = bbands.iloc[::-1]


    bbands.drop('Real Middle Band', axis=1, inplace=True)

    bbands['Average'] = average['close']
    for i in range(len(bbands.index)): 
        if (bbands['Real Upper Band'][i] - bbands['Average'][i] < 2): #sell
            initialInvestment = b.sell(51, float(bbands['Average'][i]))

        elif (bbands['Average'][i] - bbands['Real Lower Band'][i] < 2): #buy
            initialInvestment = b.buy(51, float(bbands['Average'][i]))

    print(b.get_returns())


# def vwap():
#     vwap = pd.read_csv('vwap.csv', index_col='time', parse_dates=True)
#     intraday = pd.read_csv('intraday.csv', index_col='timestamp', parse_dates=True)

#     vwap = vwap.iloc[::-1]
#     intraday = intraday.iloc[::-1]

#     vwap['Average'] = intraday['close']
#     vwap.plot()
#     # for i in range(len(bbands.index)): 
#     #     if (vwap['vwap'][i] - vwap['Average'][i] < 0.1 && ): #sell
#     #         initialInvestment = b.sell(51, float(vwap['Average'][i]))

#     #     elif (bbands['Average'][i] - bbands['Real Lower Band'][i] < 2): #buy
#     #         initialInvestment = b.buy(51, float(bbands['Average'][i]))
    

bbands()
plt.show()