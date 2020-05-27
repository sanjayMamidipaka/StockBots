import requests, json
import matplotlib.pyplot as plt
import time
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import math, backtester
import alpaca_trade_api as tradeapi
import tulipy as ti, numpy as np

def create_order(symbol, qty, side, type, time_in_force):
    api.submit_order(
        symbol= symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force
)

APCA_API_KEY_ID = 'PKNUSX6NS0QEFHBETEOP'
APCA_API_SECRET_KEY = '4ahild/ogj1pZZxrRF9Khn4tcgYmA8fNZg04Rfih'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()


initialInvestment = 1000.0
stopprofit = 0
stoploss = 0
b = backtester.Backtester(initialInvestment)
original = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
original.drop(['high','low','close','volume'], axis=1, inplace=True)
original = original[0:150]

for i in range(100000):
    now = datetime.now()
    # dd/mm/YY H:M:S
    dtstring = now.strftime("%Y-%m-%d %H:%M:%S")
    f = ''
    r = requests.get('https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch')
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    original.iloc[0] = [dtstring, float(f)]
    initial = pd.DataFrame(original) #create a new dataframe to use
    try:
        bband1 = ti.bbands(np.array(initial['open']), 50, 2)[0]
        bband2 = ti.bbands(np.array(initial['open']), 200, 2)[2]
        rsi_26 = ti.rsi(np.array(initial['open']), 26)
        ema_50 = ti.ema(np.array(initial['open']), 50)
        ema_200 = ti.ema(np.array(initial['open']), 200)
        bbands = pd.concat([pd.DataFrame(bband1),pd.DataFrame(bband2),pd.DataFrame(rsi_26), pd.DataFrame(ema_50), pd.DataFrame(ema_200)], axis=1)
        initial = pd.concat([initial, bbands], axis = 1)
        initial.columns = ['Time', 'open', 'bband1', 'bband2', 'rsi', 'ema1','ema2']
        one = int(initial['ema1'][i] >= initial['ema2'][i]) #ema
        two = int(initial['rsi'][i] <= 30)
        three = int(initial['open'][i] - initial['bband1'][1] <= 0.01)
        total = one + two + three

        newOne = int(initial['ema1'][i] >= initial['ema2'][i])
        newTwo = int(initial['rsi'][i] >= 70)
        newThree = int(initial['bband1'][1] - initial['open'][i] <= 0.01)
        newTotal = newOne + newTwo + newThree
                        
        if (total >= 2): #buy
            if b.buy(4, float(initial['open'][i]), i):
                pass
                #print(create_order('MSFT', 4, 'buy', 'market', 'gtc'))

        elif (newTotal >= 2): #sell
            if b.sell(4, initial['open'][i], i):
                pass
                #print(create_order('MSFT', 4, 'sell', 'market', 'day'))
        else:
            print('no trade executed')
    except Exception as e:
        print(e)
    time.sleep(15)

                
        
