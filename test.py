import requests, json
from bs4 import BeautifulSoup
import bs4



r = requests.get('https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch')
soup = bs4.BeautifulSoup(r.text, 'lxml')
f = soup.find_all('td')

for i in range(len(f)):
    print(i, f[i])

open = float(f[3].text.replace(',',''))
volume = float(f[13].text.replace(',',''))
print(val)