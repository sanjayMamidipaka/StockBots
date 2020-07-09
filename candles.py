import requests, json
url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-15560575-001/instruments/GBP_USD/candles?granularity=S5&price=BA'
auth_token = '6851735fed54c0315497c6a103297127-f7f82230f0c38eb85f95bdbb816dfc85'
hed = {'Authorization': 'Bearer ' + auth_token,
        "Content-Type": "application/json"}

buy = requests.get(url, headers=hed)

content = json.loads(buy.content)

#print(float(content['candles'][-1]))
print(content['candles'][-1]['bid']['c'], content['candles'][-1]['ask']['c'])