import websocket, json
import pandas as pd
import numpy as np
import pandas_ta as ta
import alpaca_trade_api as tradeapi
import backtester
# {"action": "authenticate","data": {"key_id": "PKNUSX6NS0QEFHBETEOP", "secret_key": "4ahild/ogj1pZZxrRF9Khn4tcgYmA8fNZg04Rfih"}}

# {"action": "listen", "data": {"streams": ["AM.SPY"]}}

def create_order(symbol, qty, side, type, time_in_force):
    api.submit_order(
        symbol= symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force
)

def on_open(ws):
    print('opened')
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": API_KEY, "secret_key": SECRET_KEY}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["AM.MSFT"]}}

    ws.send(json.dumps(listen_message)) 

def on_message(ws, message):
    if i % 15 == 0:
        print('received message')
        print(message)
        new_dict = {}
        info_dict = json.loads(message)
        open_price = 0.0
        for key, value in info_dict:
            if key == 'o':
                new_dict['open'] = float(value)
                open_price = float(value)
            elif key == 'h':
                new_dict['high'] = float(value)
            elif key == 'l':
                new_dict['low'] = float(value)
            elif key == 'c':
                new_dict['close'] = float(value)
            elif key == 'v':
                new_dict['volume'] = float(value)

        bbands = ta.bbands(initial['close'], length=200, std=2) #calculating indicators
        ema_50 = ta.ema(initial['close'], length=50)[-1]
        ema_200 = ta.ema(initial['close'], length=200)[-1]
        rsi_26 = ta.rsi(initial['close'], length=26)[-1]
        vwap = ta.vwap(initial['high'], initial['low'], initial['close'], initial['volume'])[-1]
        new_dict['bband1'] = bbands[0][-1]
        new_dict['bband2'] = bbands[2][-1]
        new_dict['ema_50'] = ema_50
        new_dict['ema_200'] = ema_200
        new_dict['rsi_26'] = rsi_26
        new_dict['vwap'] = vwap
        initial.append(new_dict)
        initial.columns =['timestamp', 'open', 'high', 'low', 'close', 'volume', 'bband1', 'bband2', 'ema1', 'ema2', 'rsi_26', 'vwap']

        one = int(ema_50 > ema_200) #ema
        two = int(rsi_26 < 30) # rsi
        three = int(open_price - bbands[0][-1] <= 0.01 or open_price < bbands[0][-1]) #bollinger bands
        four = int(open_price <= vwap)
        total = one + two + three + four

        newOne = int(ema_200 > ema_50)
        newTwo = int(rsi_26 > 70)
        newThree = int(bbands[2][-1] - open_price <= 0.01 or open_price > bbands[2][-1])
        newFour = int(open_price >= vwap)
        newTotal = newOne + newTwo + newThree + newFour
                        
        if (total >= 3): #buy
            if b.buy(5, open_price, i):
                create_order('MSFT', 5, 'buy', 'market', 'gtc')
                print('BUY')
        elif (newTotal >= 3): #sell
            if b.sell(5, open_price, i):
                create_order('MSFT', 5, 'sell', 'market', 'day')
                print('SELL')


socket = 'wss://data.alpaca.markets/stream'
API_KEY= 'PKNUSX6NS0QEFHBETEOP'
SECRET_KEY = '4ahild/ogj1pZZxrRF9Khn4tcgYmA8fNZg04Rfih'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()

initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial = initial[::-1].reset_index()
initial = initial[-250:]
i = 0
b = backtester.Backtester(1000)



ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()
#figure out where and when to analyze data and how
