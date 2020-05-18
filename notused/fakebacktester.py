import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np


class FakeBacktester(object):


    def __init__(self, init, dataset):
        self.first = init
        self.initialInvestment = init
        self.buys = 0
        self.sells = 0
        self.currentSells = 0
        self.dataset = dataset
    def sell(self, shares, price, i):
        if self.buys - self.sells >= 1 and self.buys > 0: #checks to make sure that you have bought something and that you currently have more buys than sells
            self.initialInvestment += (shares * price)
            self.sells += shares
            self.buys  = 0
            #print(self.dataset['minute'][i], self.dataset['close'][i], 'SELL', str(shares))
            return True
        return False

    def buy(self, shares, price, i):
        if (not (price*shares > self.initialInvestment)):
            self.buys += shares
            self.sells  = 0
            self.initialInvestment -= (shares * price)
            #print(self.dataset['minute'][i], self.dataset['close'][i], 'BUY', str(shares))
            return True
        return False

    def get_returns(self):
        return self.initialInvestment - self.first

    def get_current_buys(self):
        return self.buys - self.sells

        
        

    

