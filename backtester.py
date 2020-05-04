import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

class Backtester(object):

    def __init__(self, init):
        self.first = init
        self.initialInvestment = init

    def sell(self, shares, price):
        self.initialInvestment += (shares * price)
        #print(bbands.index[i], bbands['Average'][i], 'SELL')
        return self.initialInvestment

    def buy(self, shares, price):
        self.initialInvestment -= (shares * price)
        #print(bbands.index[i], bbands['Average'][i], 'BUY')
        return self.initialInvestment

    def get_returns(self):
        return 'Profit: ' + str(self.initialInvestment - self.first)
        

    

