import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

bbands = pd.read_csv('bbands.csv', index_col='time', parse_dates=True)
average = pd.read_csv('total.csv', index_col='timestamp', parse_dates=True)

average = average.iloc[::-1]
bbands = bbands.iloc[::-1]

bbands.drop('Real Middle Band', axis=1, inplace=True)
bbands['Average'] = average['close']


class Backtester(object):


    def __init__(self, init):
        self.first = init
        self.initialInvestment = init
        self.buys = 0

    def sell(self, shares, price, i):
        if self.buys > 0:
            self.initialInvestment += (shares * price)
            print(bbands.index[i], bbands['Average'][i], 'SELL', self.initialInvestment)
            self.buys -= 1
            return self.initialInvestment

    def buy(self, shares, price, i):
        if (not (price*shares > self.initialInvestment)):
            self.buys += 1
            self.initialInvestment -= (shares * price)
            print(bbands.index[i], bbands['Average'][i], 'BUY', self.initialInvestment)
            return self.initialInvestment

    def get_returns(self):
        return 'Profit: ' + str(self.initialInvestment - self.first)

        
        

    

