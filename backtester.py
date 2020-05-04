import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np


class Backtester(object):


    def __init__(self, init, indicator):
        self.first = init
        self.initialInvestment = init
        self.buys = 0
        self.borrows = 0
        self.indicator = indicator

    def sell(self, shares, price, i):
        if self.buys > 0:
            self.initialInvestment += (shares * price)
            print(self.indicator.index[i], self.indicator['Average'][i], 'SHORT')
        return self.initialInvestment

    def buy(self, shares, price, i):
        if (not (price*shares > self.initialInvestment)):
            self.buys += 1
            self.initialInvestment -= (shares * price)
            print(self.indicator.index[i], self.indicator['Average'][i], 'BUY')
        return self.initialInvestment

    def get_returns(self):
        return 'Profit: ' + str(self.initialInvestment - self.first)

        
        

    

