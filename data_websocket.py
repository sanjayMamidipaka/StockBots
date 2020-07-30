import websocket, json
import pandas as pd
import numpy as np
import pandas_ta as ta
import alpaca_trade_api as tradeapi
import backtester
from datetime import datetime
from datetime import timedelta
from scipy.signal import find_peaks, find_peaks_cwt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pickle

def create_order(symbol, qty, side, type, time_in_force):
    api.submit_order(
        symbol= symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force
)

def on_open(ws):
    print('open')
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": API_KEY, "secret_key": SECRET_KEY}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["AM.MSFT"]}}

    ws.send(json.dumps(listen_message)) 

def on_message(ws, message):
    global initial
    global i
    global indicators
    global buy_price
    try:
        i += 1
        checked = False
        new_dict = {}
        indic_dict = {}
        info_dict = json.loads(message)
        info_dict = info_dict['data']
        close_price = 0.0
        for key, value in info_dict.items():
            if key == 'o':
                new_dict['open'] = float(value)
                indic_dict['open'] = float(value)
            elif key == 'h':
                new_dict['high'] = float(value)
                indic_dict['high'] = float(value)
            elif key == 'l':
                new_dict['low'] = float(value)
                indic_dict['low'] = float(value)
            elif key == 'c':
                new_dict['close'] = float(value)
                indic_dict['close'] = float(value)
                checked = True
                close_price = float(value)
            elif key == 'vw':
                new_dict['vwap'] = float(value)
                indic_dict['vwap'] = float(value)

        if checked:
            initial = initial.append(new_dict, ignore_index=True)
            print(initial.tail())

        if i > 55:
            bbands = ta.bbands(initial['close'], length=50, std=2) #calculating indicators
            ema_50 = np.array(ta.ema(initial['close'], length=5))[-1]
            ema_200 = np.array(ta.ema(initial['close'], length=20))[-1]
            ema_500 = np.array(ta.ema(initial['close'], length=50))[-1]
            #macd = ta.macd(initial['close'], 5, 35, 5)
            indic_dict['bband1'] = bbands['BBL_50'].iloc[-1]
            indic_dict['useless'] = bbands['BBM_50'].iloc[-1]
            indic_dict['bband2'] = bbands['BBU_50'].iloc[-1]
            indic_dict['ema1'] = ema_50
            indic_dict['ema2'] = ema_200
            indic_dict['ema3'] = ema_500
            # indic_dict['macd'] = macd['MACD_5_35_5'].iloc[-1] 
            # indic_dict['macdh'] = macd['MACDH_5_35_5'].iloc[-1] 
            # indic_dict['macds'] = macd['MACDS_5_35_5'].iloc[-1] 
            if checked:
                indicators = indicators.append(indic_dict, ignore_index=True)
            
                pred = rfc.predict([indicators.iloc[-1]]) #PREDICT
                print(indicators.tail())
                                    
                if (pred[0] > indicators['close'].iloc[-1] and i > 5): #buy
                    if b.buy(5, close_price, 5):
                        create_order('MSFT', 5, 'buy', 'market', 'gtc')
                        buy_price = close_price
                elif (pred[0] < indicators['close'].iloc[-1] and i > 5): #sell
                    if b.sell(5, close_price, 5):
                        create_order('MSFT', 5, 'sell', 'market', 'day')
                elif (buy_price - close_price >= 0.5 and i > 5): #sell
                    if b.sell(5, close_price, 5):
                        create_order('MSFT', 5, 'sell', 'market', 'day')

            predictions.append(pred)

    except Exception as e:
        print(e)

socket = 'wss://data.alpaca.markets/stream'
API_KEY= 'PKOT8ZWPLGJ94Q705388'
SECRET_KEY = 'GgjCthiFXfl8b05cMsdZ4uhZ2aekaMNgX2ZzPB3T'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()

indicators = pd.DataFrame()
i = 0
b = backtester.Backtester(12000)
X_test = pd.DataFrame()
initial = pd.DataFrame()
from sklearn.ensemble import RandomForestRegressor
rfc = RandomForestRegressor(n_estimators=100)
predictions = [209.8]
buy_price = 0.0
with open('stock_model.pkl', 'rb') as file:
    rfc = pickle.load(file)



ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()

