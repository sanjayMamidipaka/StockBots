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
from sklearn.metrics import classification_report, confusion_matrix
from scipy.signal import find_peaks, find_peaks_cwt
from sklearn.model_selection import train_test_split
import pickle

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

        return float(content['candles'][-1]['mid']['o']), float(content['candles'][-1]['mid']['h']), float(content['candles'][-1]['mid']['l']), float(content['candles'][-1]['mid']['c']) #close first, close second
    except Exception as e:
        return 1.257
    # r = requests.get('https://finance.yahoo.com/quote/GBPUSD=X/')
    # soup = bs4.BeautifulSoup(r.text, 'lxml')
    # f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    # return float(f)

def get_decisions(close_column, distance):
    first = 0
    last = 20
    valleys = []
    peaks = []
    closes = close_column
    while last < len(initial.index):
        index = initial.index[first:last]
        temp = closes[first:last]
        valleys.append(index[np.argmin(temp)])
        peaks.append(index[np.argmax(temp)])
        first = first + distance
        last = last + distance


    decisions = [(np.nan) for i in range(len(initial.index))]
    for i in range(len(valleys)):
        decisions[valleys[i]] = 0

    for i in range(len(peaks)):
        decisions[peaks[i]] = 1

    return decisions


# initial = pd.read_csv('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=aud&to_symbol=USD&interval=1min&apikey=OUMVBY0VK0HS8I9E&outputsize=full&datatype=csv')
# initial = initial[::-1]
# initial.drop('timestamp', axis=1, inplace=True)
# bbands = ta.bbands(initial['close'], length=50, std=2) #calculating indicators
# ema_5 = ta.ema(initial['close'], length=5)
# ema_20 = ta.ema(initial['close'], length=20)
# ema_50 = ta.ema(initial['close'], length=50)
# macd = ta.macd(initial['close'], 5, 35, 5)
# rsi = ta.rsi(initial['close'], 14)
# initial = pd.concat([initial, bbands, ema_5, ema_20, ema_50, macd, rsi], axis=1)
# initial.columns =['open', 'high', 'low', 'close', 'bband1', 'useless', 'bband2', 'ema1', 'ema2', 'ema3', 'macd', 'macdh', 'macds', 'rsi']

# initial['decisions'] = get_decisions(initial['close'], 10)
# initial = initial.dropna()
# X = initial.drop(['decisions'], axis=1)
# y = initial['decisions']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle = False, stratify = None)
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100)
X_test = pd.DataFrame()
# rfc.fit(X_train, y_train) #TRAIN

b = backtester.Backtester(1000)
# initial_wait = datetime.now() + timedelta(minutes=30)
# initial_wait = initial_wait.strftime("%Y-%m-%d %H:%M:%S")
indicators = pd.DataFrame()
# initial.drop(['decisions', 'open', 'high', 'low'], axis=1, inplace=True)
with open('forex_model.pkl', 'rb') as file:
    rfc = pickle.load(file)

for i in range(10000):
    now = datetime.now()
    # dd/mm/YY H:M:S
    new_dict = {}
    indic_dict = {}
    open1, high, low, close = get_close()
    new_dict['open'] = float(open1)
    new_dict['high'] = float(high)
    new_dict['low'] = float(low)
    new_dict['close'] = float(close)
    X_test = X_test.append(new_dict, ignore_index=True)
    if i < 35:
        print(X_test.tail())

    if i >= 35:
        bbands_close = ta.bbands(X_test['close'], length=50, std=2) #calculating indicators
        macd_close = ta.macd(X_test['close'], 5, 35, 5)
        rsi_close = np.array(ta.rsi(X_test['close'], 14))[-1]
        ema_5_close = np.array(ta.ema(X_test['close'], 5))[-1]
        ema_20_close = np.array(ta.ema(X_test['close'], 20))[-1]
        ema_50_close = np.array(ta.ema(X_test['close'], 50))[-1]
        indic_dict['open'] = float(open1)
        indic_dict['high'] = float(high)
        indic_dict['low'] = float(low)
        indic_dict['close'] = float(close)
        indic_dict['useless'] = bbands_close['BBM_50'].iloc[-1]
        indic_dict['bband1'] = bbands_close['BBL_50'].iloc[-1]
        indic_dict['bband2'] = bbands_close['BBU_50'].iloc[-1] #BUYS BUYS BUYS
        indic_dict['macd'] = macd_close['MACD_5_35_5'].iloc[-1]
        indic_dict['macdh'] = macd_close['MACDH_5_35_5'].iloc[-1]
        indic_dict['macds'] = macd_close['MACDS_5_35_5'].iloc[-1]
        indic_dict['rsi'] = rsi_close
        indic_dict['ema1'] = ema_5_close
        indic_dict['ema2'] = ema_20_close
        indic_dict['ema3'] = ema_50_close
        indicators = indicators.append(indic_dict, ignore_index=True)
        pred = rfc.predict([indicators.iloc[-1]]) #PREDICT
        bs = rfc.predict_proba([indicators.iloc[-1]])
        print(indicators.tail(), pred, bs)

        if (pred == 0 and i > 5): #buy
            if b.buy(5, float(close), 5):
                buy()
        elif (pred == 1 and i > 5): #sell
            if b.sell(5, float(close), 5):
                sell()


    if i < 35:
        time.sleep(150)
    else:
        time.sleep(300)


