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
max = 200
b = backtester.Backtester(initialInvestment)
final = []

for i in range(100000):
    print(i)
    now = datetime.now()
    # dd/mm/YY H:M:S
    dtstring = now.strftime("%Y-%m-%d %H:%M:%S")
    f = ''
    r = requests.get('https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch')
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    if i <= max:
        final.append({'timestamp': dtstring, 'open': float(f), 'bband1': 0.0, 'bband2': 0.0, 'rsi': 0.0, 'ema1': 0.0, 'ema2': 0.0})
        time.sleep(30)
    else:

        bband1 = ti.bbands(np.array(initial['open']), 200, 2)[0][-1]
        bband2 = ti.bbands(np.array(initial['open']), 200, 2)[2][-1]
        rsi_26 = ti.rsi(np.array(initial['open']), 26)[-1]
        ema_50 = ti.ema(np.array(initial['open']), 50)[-1]
        ema_200 = ti.ema(np.array(initial['open']), 200)[-1]

        final.append({'timestamp': dtstring, 'open': float(f), 'bband1': bband1, 'bband2': bband2, 'rsi': rsi_26, 'ema1': ema_50, 'ema2': ema_200})
        initial = pd.DataFrame(final)

        initial.columns = ['timestamp', 'open', 'bband1', 'bband2', 'rsi', 'ema1','ema2']
        print(initial.tail())
        one = int(initial['ema1'][i] >= initial['ema2'][i]) #ema
        two = int(initial['rsi'][i] <= 30) #rsi
        three = int(initial['open'][i] - initial['bband1'][i] <= 0.01) #bbands
        total = one + two + three

        newOne = int(initial['ema1'][i] <= initial['ema2'][i]) #ema
        newTwo = int(initial['rsi'][i] >= 70) #rsi
        newThree = int(initial['bband1'][i] - initial['open'][i] <= 0.01) # bbands
        newTotal = newOne + newTwo + newThree
                        
        if (total >= 2): #buy
            if b.buy(5, float(initial['open'][i]), 0):
                print(create_order('MSFT', 5, 'buy', 'market', 'gtc'))

        elif (newTotal >= 2 or initial['open'][i] >= stopprofit or initial['open'][i] < stoploss): #sell
            if b.sell(5, initial['open'][i], 0):
                print(create_order('MSFT', 5, 'sell', 'market', 'day'))
        else:
            print('no trade executed')
        time.sleep(60)
    
    stopprofit = initial['open'][i] * 1 + (0.005)
    stoploss = initial['open'][i] * 1 - (0.005)

    

                
        
