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
final = []
f = ''
initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=work&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial.drop(['high','low','close','volume'], axis=1, inplace=True)
initial = initial[::-1].reset_index()
initial.drop(['index'], axis=1, inplace=True)
initial = initial[-250:]
for i in range(100000):
    try:
        now = datetime.now()
        # dd/mm/YY H:M:S
        dtstring = now.strftime("%Y-%m-%d %H:%M:%S")
        r = requests.get('https://finance.yahoo.com/quote/WORK')
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    except Exception as e:
        print(e)

    bband1 = ti.bbands(np.array(initial['open']), 50, 2)[0][-1]
    bband2 = ti.bbands(np.array(initial['open']), 50, 2)[2][-1]
    rsi_26 = ti.rsi(np.array(initial['open']), 14)[-1]
    ema_50 = ti.ema(np.array(initial['open']), 50)[-1]
    ema_200 = ti.ema(np.array(initial['open']), 200)[-1]

    initial = initial.append({'timestamp': dtstring, 'open': float(f), 'bband1': bband1, 'bband2': bband2, 'rsi': rsi_26, 'ema1': ema_50, 'ema2': ema_200}, ignore_index=True)
    print(initial.tail())


    initial.columns = ['timestamp', 'open', 'bband1', 'bband2', 'rsi', 'ema1','ema2']
    one = int(ema_50 > ema_200) #ema
    two = int(rsi_26 < 30) # rsi
    three = int(float(f) - bband1 <= 0.01 or float(f) < bband1) #bollinger bands
    total = one + two + three

    newOne = int(ema_200 > ema_50)
    newTwo = int(rsi_26 > 70)
    newThree = int(bband2 - float(f) <= 0.01 or float(f) > bband2)
    newTotal = newOne + newTwo + newThree
                    
    if (total >= 2 and i > 10): #buy
        if b.buy(5, float(f), i):
            create_order('WORK', 5, 'buy', 'market', 'gtc')
            print('BUY')
    elif (newTotal >= 2 and i > 10): #sell
        if b.sell(5, float(f), i):
            create_order('WORK', 5, 'sell', 'market', 'day')
            print('SELL')
    time.sleep(60)