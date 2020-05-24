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
import tulipy as ti, numpy as np

def create_order(symbol, qty, side, type, time_in_force):
    api.submit_order(
        symbol= symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force
)

APCA_API_KEY_ID = 'PKH035NUPC4CVI24RTPV'
APCA_API_SECRET_KEY = 'C/jeqiGRKwf2yinKPndfaqvRil1CHN2zBLZC31lP'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()



total = []
initialInvestment = 10000.0
stopprofit = 0
stoploss = 0
b = backtester.Backtester(initialInvestment)
df = pd.DataFrame()

for i in range(100000):
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    f = ''
    r = requests.get('https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch')
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text

    g = soup.find_all('td')
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    dict1 = {'Time': dt_string, 'close': float(f)}
    print(dict1)
    total.append(dict1)
    initial = pd.DataFrame(total)
    bband1 = ti.bbands(np.array(initial['open']), 26, 2)[0]
    bband2 = ti.bbands(np.array(initial['open']), 26, 2)[2]
    rsi_26 = ti.rsi(np.array(initial['open']),26)
    bbands = pd.concat([pd.DataFrame(bband1),pd.DataFrame(bband2),pd.DataFrame(rsi_26)], axis=1)
    initial = pd.concat([initial, bbands], axis = 1)
    initial = initial.iloc[::-1]
    initial.columns = ['Time', 'close', 'bband1', 'bband2', 'rsi']

    one = int(initial['open'].ewm(span=50).mean()[i] > initial['open'].ewm(span=200).mean()[i])
    two = int(initial['rsi_26'][i] <= 30)
    three = int(initial['open'][i] - initial['bband1'][1] <= 0.01)
    total = one + two + three

    newOne = int(initial['open'].ewm(span=50).mean()[i] < initial['open'].ewm(span=200).mean()[i])
    newTwo = int(initial['rsi'][i] >= 70)
    newThree = int(initial['bband1'][1] - initial['open'][i] <= 0.01)
    newTotal = newOne + newTwo + newThree
                    
    if (total >= 2): #buy
        if b.buy(math.floor(float(initialInvestment)/float(initial['open'][i])), float(initial['open'][i]), i):
            pass

    elif (newTotal >= 2 or initial['open'][i] <= stoploss or initial['open'][i] >= stopprofit): #sell
        if b.sell(b.get_current_buys(), initial['close'][i], i):
            pass
    else:
        print('no trade executed')

    stopprofit = float(initial['close'][i]) * (1 + 0.01)
    stoploss = float(initial['close'][i]) * (1 + 0.01)
    time.sleep(60)

                
        
