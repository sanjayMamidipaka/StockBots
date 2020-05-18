import requests, time
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json

def scrape(df):
    count = 0
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    f = ''
    try:
        r = requests.get('https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch')
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        count += 1
        dict1 = {'Time': dt_string, 'close': float(f)}
        total.append(dict1)
        df = pd.DataFrame(total)
        return df
    except:
        f = ''



total = []
df = pd.DataFrame()
for i in range(5):
    print(scrape(df))
