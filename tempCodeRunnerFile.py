url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
r = '{}&symbol={}&interval={}&apikey={}&datatype={}&outputsize={}'.format(url, 'TSLA', '1min','9YM6MWUWHMZN05MB', 'csv','full')

initial = pd.read_csv(r, index_col='timestamp', parse_dates=True)
initial = initial.iloc[::-1]
initial = initial[-350:]

stock = StockDataFrame.retype(initial)
initial['bband1'] = stock['boll_lb']
initial['bband2'] = stock['boll_ub']
initial['rsi'] = stock['rsi_6']