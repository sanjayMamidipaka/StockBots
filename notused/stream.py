import requests, json
import matplotlib.pyplot as plt

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': 'PKZSUP7DM38Q91F30C1S', 'APCA-API-SECRET-KEY': 'TxpuAdbLgZBPv3AeTBkqKNzpP1w/zUbVlIL035Gy'}
DATA_URL = 'https://data.alpaca.markets/v1/bars'

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force

    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)

def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

def get_data(time_period, symbol):
    r = requests.get('{}/{}?symbols={}'.format(DATA_URL, time_period, symbol), headers=HEADERS)
    return json.loads(r.content)

#response = create_order('MSFT', 1, "buy", "market", "gtc")
response = get_data('1Min', 'MSFT')


t = [0]
vwaps = [0]
vols = [response['MSFT'][0]['v']]
j = -1
for i in response['MSFT']:
    j+=1
    t.append(int(i['t']))
    typ = float((i['h'] + i['l'] + i['c'])/3)
    per_vol = typ * float(i['v'])
    vwaps.append((vwaps[j] + per_vol)/(vols[j]))
    vols.append(response['MSFT'][j]['v'])


plt.plot(t, vwaps)
plt.show()
