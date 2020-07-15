import requests, time
import bs4, numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json
import time
import pandas_ta as ta
import backtester 
from datetime import datetime, timedelta

def buy():
    url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-15560575-001/orders'
    auth_token = '6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85'
    hed = {'Authorization': 'Bearer ' + auth_token,
            "Content-Type": "application/json"}
    data = {"order": {
        "units": "800",
        "instrument": "GBP_USD",
        "timeInForce": "FOK",
        "type": "MARKET",
        "positionFill": "DEFAULT"}}

    buy = requests.post(url, headers=hed, json=data)
    print(buy.content)

def sell():
    url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-15560575-001/orders'
    auth_token = '6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85'
    hed = {'Authorization': 'Bearer ' + auth_token,
            "Content-Type": "application/json"}
    data = {"order": {
        "units": "-800",
        "instrument": "GBP_USD",
        "timeInForce": "FOK",
        "type": "MARKET",
        "positionFill": "DEFAULT"}}

    sell = requests.post(url, headers=hed, json=data)
    print(sell.content)

def get_close():
    try:
        url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-15560575-001/instruments/GBP_USD/candles?price=M&granularity=M1&count=1'
        auth_token = '6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85'
        hed = {'Authorization': 'Bearer ' + auth_token,
                "Content-Type": "application/json"}

        buy = requests.get(url, headers=hed)

        content = json.loads(buy.content)

        return float(content['candles'][-1]['mid']['c']) #ask first, ask second
    except Exception as e:
        return 1.257
    # r = requests.get('https://finance.yahoo.com/quote/GBPUSD=X/')
    # soup = bs4.BeautifulSoup(r.text, 'lxml')
    # f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    # return float(f)


initial = pd.DataFrame(columns=['timestamp', 'ask'])
indicators = pd.DataFrame(columns = ['bband1_ask', 'bband2_ask', 'macd_ask', 'macdh_ask', 'macds_ask', 'rsi_ask'])
total = []
bought_ask = get_close()
b = backtester.Backtester(1000)
initial_wait = datetime.now() + timedelta(minutes=1)
initial_wait = initial_wait.strftime("%Y-%m-%d %H:%M:%S")
sell_status = 0

for i in range(10000):
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    f = ''
    new_dict = {}
    buys = [0]
    indic_dict = {}
    ask = get_close()
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    new_dict['timestamp'] = dt_string
    new_dict['ask'] = float(ask)
    initial = initial.append(new_dict, ignore_index=True)
    print(initial.tail())

    if i > 50:
        bbands_ask = ta.bbands(initial['ask'], length=30, std=2) #calculating indicators
        macd_ask = ta.macd(initial['ask'], 5, 35, 5)
        rsi_ask = np.array(ta.rsi(initial['ask'], 10))[-1]
        ema_5_ask = np.array(ta.ema(initial['ask'], 5))[-1]
        ema_20_ask = np.array(ta.ema(initial['ask'], 20))[-1]
        ema_50_ask = np.array(ta.ema(initial['ask'], 50))[-1]
        indic_dict['bband1_ask'] = bbands_ask['BBL_30'].iloc[-1]
        indic_dict['bband2_ask'] = bbands_ask['BBU_30'].iloc[-1] #BUYS BUYS BUYS
        indic_dict['macd_ask'] = macd_ask['MACD_5_35_5'].iloc[-1] 
        indic_dict['macdh_ask'] = macd_ask['MACDH_5_35_5'].iloc[-1] 
        indic_dict['macds_ask'] = macd_ask['MACDS_5_35_5'].iloc[-1]
        indic_dict['rsi_ask'] = rsi_ask
        indic_dict['ema_5_ask'] = ema_5_ask
        indic_dict['ema_20_ask'] = ema_20_ask
        indic_dict['ema_50_ask'] = ema_50_ask

        indicators = indicators.append(indic_dict, ignore_index=True)
        print(indicators.tail())

        one = int(ema_5_ask > ema_20_ask and ema_20_ask > ema_50_ask)
        two = int(macd_ask['MACD_5_35_5'].iloc[-1] >= macd_ask['MACDS_5_35_5'].iloc[-1] and macd_ask['MACDH_5_35_5'].iloc[-1] >= 0) #macd
        three = int(float(ask) <= bbands_ask['BBL_30'].iloc[-1]) #bollinger bands
        four = int(rsi_ask <= 30) #rsi
        total = one + two + three + four
        print('Total:', total)

        newOne = int(ema_5_ask < ema_20_ask and ema_20_ask < ema_50_ask)
        newTwo = int(macd_ask['MACD_5_35_5'].iloc[-1] < macd_ask['MACDS_5_35_5'].iloc[-1] and macd_ask['MACDH_5_35_5'].iloc[-1] < 0) #macd
        newThree = int(float(ask) >= bbands_ask['BBU_30'].iloc[-1]) #bbands
        newFour = int(rsi_ask >= 70) #rsi
        newTotal = newOne + newTwo + newThree + newFour
        print('newTotal:', newTotal)

        if (total >= 3 and new_dict['timestamp'] > initial_wait): #buy
            if b.buy(5, float(ask), 5):
                buy()
                buys.append(float(ask))

        elif (newTotal >= 3 and new_dict['timestamp'] > initial_wait): #sell
            if b.sell(5, float(ask), 5):
                sell()


    time.sleep(60)


    