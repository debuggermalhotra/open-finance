'''Commodity Channel Index (CCI)
   CCI = (Typical price – MA of Typical price) / (0.015 * Standard deviation of Typical price)
   A bullish divergence occurs when the underlying security makes a lower low and the CCI forms a higher low, 
   which shows less downside momentum. Similarly, a bearish divergence is formed when the security records 
   a higher high and the CCI forms a lower high, which shows less upside momentum.
'''

import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from kloudtrader.defaults import *
from kloudtrader.equities.data import *



data=OHLCV('AAPl',"2014-01-01","2016-01-01")['history']['day']
data = pd.DataFrame(data)

def CCI(data, number_of_days):
    TP = (data['high'] + data['low'] + data['close']) / 3  #Typical Price (Average of high, low and close prices)
    CCI=pd.Series(TP.rolling(number_of_days).mean()/ (0.015 * TP.rolling(number_of_days).std()),name='CCI')
    data = data.join(CCI) 
    return data

AAPL_CCI = CCI(data, number_of_days=20)
CCI = AAPL_CCI['CCI']

trace0 = go.Scatter(
    x = data['date'],
    y = data['close'],
    mode = 'lines',
    name = 'Close Prices'
)
trace1 = go.Scatter(
    x = data['date'],
    y = AAPL_CCI['CCI'],
    mode = 'lines',
    name = 'CCI'
)

data1 = [trace0, trace1]

py.plot(data1)


#py.plot(data, filename='CCI')