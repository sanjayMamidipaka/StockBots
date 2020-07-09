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
    url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-15560575-001/instruments/GBP_USD/candles?price=BA&granularity=S5&count=1'
    auth_token = '6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85'
    hed = {'Authorization': 'Bearer ' + auth_token,
            "Content-Type": "application/json"}

    buy = requests.get(url, headers=hed)

    content = json.loads(buy.content)

    return [float(content['candles'][-1]['ask']['c']), float(content['candles'][-1]['bid']['c'])] #ask first, bid second
    # r = requests.get('https://finance.yahoo.com/quote/GBPUSD=X/')
    # soup = bs4.BeautifulSoup(r.text, 'lxml')
    # f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    # return float(f)


initial = pd.read_csv('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=gbp&to_symbol=usd&interval=1min&apikey=OUMVBY0VK0HS8I9E&outputsize=full&datatype=csv')
initial = initial[::-1]
initial['bid'] = initial['close']
initial = initial.drop(['open','high','low'], axis=1)
initial.columns = ['timestamp', 'ask', 'bid']
initial = initial[-205:]
total = []
bought_bid = get_close()[0]
bought_ask = get_close()[1]
b = backtester.Backtester(1000)
initial_wait = datetime.now() + timedelta(minutes=15)
initial_wait = initial_wait.strftime("%Y-%m-%d %H:%M:%S")

for i in range(10000):
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    f = ''
    new_dict = {}
    ask = get_close()[0]
    bid = get_close()[1]
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    new_dict['timestamp'] = dt_string
    new_dict['bid'] = float(bid)
    new_dict['ask'] = float(ask)
    bbands_ask = ta.bbands(initial['ask'], length=50, std=2) #calculating indicators
    ema_50_ask = np.array(ta.ema(initial['ask'], length=5))[-1]
    ema_200_ask = np.array(ta.ema(initial['ask'], length=20))[-1]
    ema_500_ask = np.array(ta.ema(initial['ask'], length=50))[-1]
    macd_ask = ta.macd(initial['ask'], 12, 26, 9)
    rsi_ask = np.array(ta.rsi(initial['ask'], 28))[-1]
    new_dict['bband1_ask'] = bbands_ask['BBL_50'].iloc[-1]
    new_dict['bband2_ask'] = bbands_ask['BBU_50'].iloc[-1] #BUYS BUYS BUYS
    new_dict['hma_50_ask'] = ema_50_ask
    new_dict['hma_200_ask'] = ema_200_ask
    new_dict['hma_500_ask'] = ema_500_ask
    new_dict['macd_ask'] = macd_ask['MACD_12_26_9'].iloc[-1] 
    new_dict['macdh_ask'] = macd_ask['MACDH_12_26_9'].iloc[-1] 
    new_dict['macds_ask'] = macd_ask['MACDS_12_26_9'].iloc[-1]
    new_dict['rsi_ask'] = rsi_ask

    bbands_bid = ta.bbands(initial['bid'], length=50, std=2) #calculating indicators
    ema_50_bid = np.array(ta.ema(initial['bid'], length=5))[-1]
    ema_200_bid = np.array(ta.ema(initial['bid'], length=20))[-1]
    ema_500_bid = np.array(ta.ema(initial['bid'], length=50))[-1]
    macd_bid = ta.macd(initial['bid'], 12, 26, 9)
    rsi_bid = np.array(ta.rsi(initial['bid'], 28))[-1]
    new_dict['bband1_bid'] = bbands_bid['BBL_50'].iloc[-1]
    new_dict['bband2_bid'] = bbands_bid['BBU_50'].iloc[-1] #SELLS SELLS SELLS
    new_dict['hma_50_bid'] = ema_50_bid
    new_dict['hma_200_bid'] = ema_200_bid
    new_dict['hma_500_bid'] = ema_500_bid
    new_dict['macd_bid'] = macd_bid['MACD_12_26_9'].iloc[-1] 
    new_dict['macdh_bid'] = macd_bid['MACDH_12_26_9'].iloc[-1] 
    new_dict['macds_bid'] = macd_bid['MACDS_12_26_9'].iloc[-1]
    new_dict['rsi_bid'] = rsi_bid

    initial = initial.append(new_dict, ignore_index=True)
    print(initial.tail())

    one = int(ema_50_ask >= ema_200_ask and ema_200_ask >= ema_500_ask) #ema
    two = int(macd_ask['MACD_12_26_9'].iloc[-1] >= macd_ask['MACDS_12_26_9'].iloc[-1] and macd_ask['MACDH_12_26_9'].iloc[-1] >= 0) #rsi
    three = int(float(ask) - bbands_ask['BBL_50'].iloc[-1] <= 0.01 or float(ask) <= bbands_ask['BBL_50'].iloc[-1]) #bollinger bands
    four = int(rsi_ask <= 30)
    total = one + two + three + four
    print('Total:', total)

    newOne = int(ema_50_bid < ema_200_bid and ema_200_bid < ema_500_bid)
    newTwo = int(macd_bid['MACD_12_26_9'].iloc[-1] < macd_bid['MACDS_12_26_9'].iloc[-1] and macd_bid['MACDH_12_26_9'].iloc[-1] < 0)
    newThree = int(bbands_bid['BBU_50'].iloc[-1] - float(bid) < 0.01 or float(bid) > bbands_bid['BBU_50'].iloc[-1])
    newFour = int(rsi_ask >= 70)
    newTotal = newOne + newTwo + newThree + newFour
    print('newTotal:', newTotal)

    if (total >= 3 and new_dict['timestamp'] > initial_wait): #buy
        if b.buy(5, float(ask), 5):
            buy()
            bought_ask = ask
    elif (newTotal >= 3 and new_dict['timestamp'] > initial_wait): #sell
        if b.sell(5, float(bid), 5):
            sell()
            bought_bid = bid

    time.sleep(25)

    