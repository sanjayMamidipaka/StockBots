import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np


class Backtester(object):


    def __init__(self, init):
        self.first = init
        self.initialInvestment = init
        self.buys = 0
        self.sells = 0
        self.currentSells = 0
        self.currentlyBought = 0
        self.sharpe_list = []
        self.treasury_rate = 0.0
    def sell(self, shares, price, i):
        if self.buys - self.sells >= 1 and self.buys > 0: #checks to make sure that you have bought something and that you currently have more buys than sells
            self.initialInvestment += (shares * price)
            self.sharpe_list.append((shares * price) - self.first)
            self.sells += shares
            self.buys  = 0
            self.currentlyBought = 0
            print('SELL', str(shares))
            return True
        return False

    def buy(self, shares, price, i):
        if (not (price*shares > self.initialInvestment) and self.currentlyBought < 1):
            self.buys += shares
            self.sells  = 0
            self.initialInvestment -= (shares * price)
            self.currentlyBought += 1
            print('BUY', str(shares))
            return True
        return False

    def get_returns(self):
        return self.initialInvestment - self.first

    def get_current_buys(self):
        return self.buys - self.sells

    def get_sharpe(self):
        std = np.std(np.array(self.sharpe_list))
        return (((self.initialInvestment - self.first)/self.first)*100 - self.treasury_rate)/std


        
        

    

