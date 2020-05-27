import backtester
import pandas as pd
import matplotlib.pyplot as plt
import math, numpy as np
import tulipy as ti

final = 0.0
numTrades = 0
initial = pd.read_csv('https://cloud.iexapis.com/stable/stock/msft/chart/max?token=pk_b049e8a0ad014f1e8e1e1cde420f215d&format=csv')
initial2 = initial[['label','open','high','low','close','volume']] 
bband1 = np.flipud(ti.bbands(np.array(initial['open']), 26, 2)[0])
bband2 = np.flipud(ti.bbands(np.array(initial['open']), 26, 2)[2])
rsi_26 = np.flipud(ti.rsi(np.array(initial['open']), 26))
bbands = pd.concat([pd.DataFrame(bband1),pd.DataFrame(bband2),pd.DataFrame(rsi_26)], axis=1)
initial2 = pd.concat([initial2, bbands], axis = 1)
initial2.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'bband1', 'bband2', 'rsi']


initialInvestment = 1000.0
stopprofit = float(initial['open'][0]) * (1+0.01)
stoploss = float(initial['open'][0]) * (1-0.01)

b = backtester.Backtester(initialInvestment)
for i in range(len(initial.index)-200):
    try:
        one = int(initial2['open'].ewm(span=12).mean()[i] >= initial2['open'].ewm(span=26).mean()[i]) #ema
        two = int(initial2['rsi'][i] <= 30) # rsi
        three = int(initial2['open'][i] - initial2['bband1'][i] <= 0.01) #bollinger bands
        total = one + two + three

        newOne = int(initial2['open'].ewm(span=12).mean()[i] <= initial2['open'].ewm(span=26).mean()[i])
        newTwo = int(initial2['rsi'][i] >= 70)
        newThree = int(initial2['bband1'][i] - initial2['open'][i] <= 0.01)
        newTotal = newOne + newTwo + newThree

        

        if (total >= 2): #buy
            if b.buy(math.floor(float(initialInvestment)/float(initial['open'][i])), float(initial['open'][i]), i):
                numTrades += 1
                print(initial['timestamp'][i])

        elif (newTotal >= 2 or initial['open'][i] <= stoploss or initial['open'][i] >= stopprofit): #sell
            if b.sell(b.get_current_buys(), initial['close'][i], i):
                print(initial['timestamp'][i])

        stopprofit = float(initial['open'][i-1]) * (1+0.01)
        stoploss = float(initial['open'][i-1]) * (1-0.01)
    except:
        pass



i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['close'][i], i): #sell everything once the day is done
    print('sell')



#plt.scatter(sellx, selly,c='red', label='sell')
#plt.scatter(buyx, buyy,c='green', label='buy')
#plt.legend()
print(b.get_returns())
print('Number of buy-sell pairs:', numTrades)
#plt.show()
