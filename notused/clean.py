import fakebacktester
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import requests, csv
from stockstats import StockDataFrame

initialInvestment = 15000.0
sellx = []
selly = []

buyx = []
buyy = []

allx = []
ally = []

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'msft', '1min','9YM6MWUWHMZN05MB', 'csv','full')

average = pd.read_csv(r, index_col='timestamp', parse_dates=True)

stock = StockDataFrame.retype(average)

for i in range(0,len(average.index)):
    if stock['macd'][i] == stock['macds'][i]:
        print(i)
average['close'].plot()
plt.show()