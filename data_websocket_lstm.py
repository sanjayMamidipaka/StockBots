import websocket, json
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import backtester
from datetime import datetime
from datetime import timedelta
from sklearn.preprocessing import MinMaxScaler
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
    global buy_price
    try:
        i += 1
        checked = False
        new_dict = {}
        info_dict = json.loads(message)
        info_dict = info_dict['data']
        close_price = 0.0
        for key, value in info_dict.items():
            if key == 'c':
                new_dict['close'] = float(value)
                checked = True
                close_price = float(value)

        if checked:
            initial = initial.append(new_dict, ignore_index=True)
            if i <= 55:
                print(initial.tail())

        if i > 55:
            last_60_days = initial[-60:].values
            last_60_days_scaled = scaler.transform(last_60_days)
            
            X_test = []
            X_test.append(last_60_days_scaled)
            X_test = np.array(X_test)
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            pred_price = model.predict(X_test)
            pred_price = scaler.inverse_transform(pred_price)
            predictions.append(float(pred_price))
            print(initial.tail(), pred_price)

            if (predictions[-1] > predictions[-2]): #buy
                if b.buy(5, float(close_price), 5):
                    create_order('MSFT', 5, 'buy', 'market', 'gtc')
                    buy_price = float(close_price)

            if ((float(close_price) - buy_price)*5 > 1.0 and pred_price < float(close_price)): #sell
                if b.sell(5, float(close_price), 5):
                    create_order('MSFT', 5, 'sell', 'market', 'day')

            elif ((buy_price - float(close_price))*5 >= 1.0): #sell
                if b.sell(5, float(close_price), 5):
                    create_order('MSFT', 5, 'sell', 'market', 'day')
    except Exception as e:
        print(e)

socket = 'wss://data.alpaca.markets/stream'
API_KEY= 'PKOT8ZWPLGJ94Q705388'
SECRET_KEY = 'GgjCthiFXfl8b05cMsdZ4uhZ2aekaMNgX2ZzPB3T'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()

predictions = []
i = 0
buy_price = 0.0
b = backtester.Backtester(12000)
checked = False
initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial = initial[::-1]
initial.drop(['timestamp', 'open', 'high', 'low', 'volume'], axis=1, inplace=True)
model = 1
scaler = MinMaxScaler(feature_range=(0,1))
scaler.fit(initial)
with open('lstm.pkl', 'rb') as file:
    model = pickle.load(file)



ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()

