import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')

first = 0
last = 20
valleys = []
peaks = []
closes = initial['close']
while last < len(initial.index):
    index = initial.index[first:last]
    temp = closes[first:last]
    valleys.append(index[np.argmin(temp)])
    peaks.append(index[np.argmax(temp)])
    first = first + 20
    last = last + 20


decisions = [(np.nan) for i in range(len(initial.index))]
for i in range(len(valleys)):
    decisions[valleys[i]] = 0

for i in range(len(peaks)):
    decisions[peaks[i]] = 1

initial['decisions'] = decisions
    