import requests
import json

url = 'https://api.worldtradingdata.com/api/v1/stock'
params = {
  'symbol': 'SNAP',
  'api_token': 'HeTsqbCqVwJ3wUFPv09BWm5OF3TaMby4qQ8261Pew1PEZNrbH2Ei6Unujb8T',
  'output': 'csv'
}
response = requests.request('GET', url, params=params)
print(response.content)