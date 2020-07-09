import websocket, json
import pandas as pd
import numpy as np
import pandas_ta as ta
import alpaca_trade_api as tradeapi
import backtester
from datetime import datetime
from datetime import timedelta

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
    i += 1
    checked = False
    new_dict = {}
    info_dict = json.loads(message)
    info_dict = info_dict['data']
    close_price = 0.0
    vwap_copy = 0.0 
    new_dict['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for key, value in info_dict.items():
        if key == 'o':
            new_dict['open'] = float(value)
        elif key == 'h':
            new_dict['high'] = float(value)
        elif key == 'l':
            new_dict['low'] = float(value)
        elif key == 'c':
            new_dict['close'] = float(value)
            checked = True
            close_price = float(value)
        elif key == 'vw':
            new_dict['vwap'] = float(value)
            vwap_copy = float(value)

    bbands = ta.bbands(initial['close'], length=50, std=2) #calculating indicators
    ema_50 = np.array(ta.hma(initial['close'], length=5))[-1]
    ema_200 = np.array(ta.hma(initial['close'], length=20))[-1]
    macd = ta.macd(initial['close'], 12, 26, 9)
    new_dict['bband1'] = bbands['BBL_50'].iloc[-1]
    new_dict['bband2'] = bbands['BBU_50'].iloc[-1]
    new_dict['hma_50'] = ema_50
    new_dict['hma_200'] = ema_200
    new_dict['macd'] = macd['MACD_12_26_9'].iloc[-1] 
    new_dict['macdh'] = macd['MACDH_12_26_9'].iloc[-1] 
    new_dict['macds'] = macd['MACDS_12_26_9'].iloc[-1] 
    if checked:
        initial = initial.append(new_dict, ignore_index=True)
        print(initial.tail())

    one = int(ema_50 >= ema_200) #ema
    two = int(macd['MACD_12_26_9'].iloc[-1] >= macd['MACDS_12_26_9'].iloc[-1] and macd['MACDH_12_26_9'].iloc[-1] >= 0) #rsi
    three = int(close_price - bbands['BBL_50'].iloc[-1] <= 0.01 or close_price <= bbands['BBL_50'].iloc[-1]) #bollinger bands
    four = int(close_price <= vwap_copy) #vwap
    total = one + two + three + four
    print('Total:', total)

    newOne = int(ema_50 < ema_200)
    newTwo = int(macd['MACD_12_26_9'].iloc[-1] < macd['MACDS_12_26_9'].iloc[-1] and macd['MACDH_12_26_9'].iloc[-1] < 0)
    newThree = int(bbands['BBU_50'].iloc[-1] - close_price < 0.01 or close_price > bbands['BBU_50'].iloc[-1])
    newFour = int(close_price > vwap_copy)
    newTotal = newOne + newTwo + newThree + newFour
    print('newTotal:', newTotal)
                    
    if (total >= 3 and new_dict['timestamp'] > initial_wait): #buy
        if b.buy(5, close_price, 5):
            create_order('MSFT', 5, 'buy', 'market', 'gtc')
    elif (newTotal >= 3 and new_dict['timestamp'] > initial_wait): #sell
        if b.sell(5, close_price, 5):
            create_order('MSFT', 5, 'sell', 'market', 'day')


socket = 'wss://data.alpaca.markets/stream'
API_KEY= 'PKOT8ZWPLGJ94Q705388'
SECRET_KEY = 'GgjCthiFXfl8b05cMsdZ4uhZ2aekaMNgX2ZzPB3T'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()

initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=MSFT&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial = initial[::-1].reset_index()
initial.drop(['index','volume'], axis=1, inplace=True)
initial = initial[-170:]
i = 0
b = backtester.Backtester(120000)
initial_wait = datetime.now() + timedelta(minutes = 5)
initial_wait = initial_wait.strftime("%Y-%m-%d %H:%M:%S")



ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()
