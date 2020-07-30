import requests, time
import numpy as np
from datetime import datetime
import pandas as pd
import json
import time
import backtester
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import MinMaxScaler

def buy():
    url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-15560575-001/orders'
    auth_token = '6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85'
    hed = {'Authorization': 'Bearer ' + auth_token,
            "Content-Type": "application/json"}
    data = {"order": {
        "units": "1420",
        "instrument": "AUD_USD",
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
        "units": "-1420",
        "instrument": "AUD_USD",
        "timeInForce": "FOK",
        "type": "MARKET",
        "positionFill": "DEFAULT"}}

    sell = requests.post(url, headers=hed, json=data)
    print(sell.content)

def get_close():
    try:
        url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-15560575-001/instruments/AUD_USD/candles?price=M&granularity=M1&count=1'
        auth_token = '6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85'
        hed = {'Authorization': 'Bearer ' + auth_token,
                "Content-Type": "application/json"}

        buy = requests.get(url, headers=hed)

        content = json.loads(buy.content)

        return float(content['candles'][-1]['mid']['c']) #close first, close second
    except Exception as e:
        return 1.257
    # r = requests.get('https://finance.yahoo.com/quote/GBPUSD=X/')
    # soup = bs4.BeautifulSoup(r.text, 'lxml')
    # f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    # return float(f)


initial = pd.read_csv('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=aud&to_symbol=USD&interval=1min&apikey=OUMVBY0VK0HS8I9E&outputsize=full&datatype=csv')
initial = initial[::-1]
initial.drop(['timestamp', 'open', 'high', 'low'], axis=1, inplace=True)

b = backtester.Backtester(1000)
model = 1
buy_price = 0.0
with open('forex_lstm.pkl', 'rb') as file:
    model = pickle.load(file)

scaler = MinMaxScaler(feature_range=(0,1))
scaler.fit(initial)

for i in range(10000):
    now = datetime.now()
    # dd/mm/YY H:M:S
    new_dict = {}
    close = get_close()
    new_dict['close'] = float(close)
    initial = initial.append(new_dict, ignore_index=True)
    if i < 51:
        print(initial.tail())

    if i >= 51:
        last_60_days = initial[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)
        
        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        print(initial.tail(), pred_price)

        if (pred_price > close): #buy
            if b.buy(5, float(close), 5):
                buy_price = float(close)
                buy()
        elif (close - buy_price >= 0.001): #sell
            if b.sell(5, float(close), 5):
                sell()
        if (close - buy_price <= -0.0005): #sell
            if b.sell(5, float(close), 5):
                sell()


    time.sleep(60)


