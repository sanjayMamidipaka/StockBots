import requests, json
import matplotlib.pyplot as plt
import requests, time
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json, time, math, backtester
from stockstats import StockDataFrame
import alpaca_trade_api as tradeapi

APCA_API_KEY_ID = 'PK7ZSKV6Y7F9QA8C82JJ'
APCA_API_SECRET_KEY = '/zEsiiSsm4po2a4jwyCmWcixmQNf9pKjAgqBtNcT'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()


def create_order(symbol, qty, side, type, time_in_force):
    api.submit_order(
        symbol= symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force
)

stopprofit = 54.59 + 0.2


def scrape(df):
    try:
        count = 0
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        f = ''
        r = requests.get('https://finance.yahoo.com/quote/AMD?p=AMD&.tsrc=fin-srch')
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        count += 1
        dict1 = {'Time': dt_string, 'close': float(f)}
        total.append(dict1)
        initial = pd.DataFrame(total)

        stock = StockDataFrame.retype(initial)
        initial['bband1'] = stock['boll_lb']
        initial['bband2'] = stock['boll_ub']
                        
        if ((stock['rsi_6'][i] < 45 and initial['close'][i] - initial['bband1'][i] < 0.1)): #buy
            if b.buy(math.floor(initialInvestment/initial['close'][i]), initial['close'][i], i):
                print(create_order('AMD', 9, 'buy', 'market', 'gtc'))

        elif ((stock['rsi_6'][i] > 60 and initial['bband2'][i] - initial['close'][i] < 0.1) or float(f) == stopprofit): #sell
            if b.sell(b.get_current_buys(), initial['close'][i], i):
                print(create_order('AMD', 9, 'sell', 'market', 'day'))
        else:
            print('no trade executed')
    except:
        print('Error!')

                
            



total = []
initialInvestment = 500.0
b = backtester.Backtester(initialInvestment)
df = pd.DataFrame()
for i in range(100000):
    time.sleep(60)
    scrape(df)
