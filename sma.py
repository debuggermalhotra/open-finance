'''If dealing with one moving average: 
    When the closing price moves above the moving average, a buy signal is generated and vice versa.
    If dealing with 2 moving averages:
    a long/buy signal is generated when the shorter average crosses above the longer average.
    Similarly, a short/sell is generated when the shorter crosses below the longer average.'''

from time import sleep
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from kloudtrader.defaults import *
from kloudtrader.equities.data import *
from wrapper import *

FUNDS=100000

def SMA(data,number_of_days):
    close=data['close']
    SMA=pd.DataFrame(close.rolling(number_of_days).mean()) 
    return SMA

def analysis(data):
    SMA20=SMA(data,20)
    SMA50=SMA(data,50)
    df=pd.DataFrame()
    df['Date']=data.date
    df['Close']=data.close
    df['SMA20']=SMA20
    df['SMA50']=SMA50
    for index,row in df.iterrows():
        if row['SMA20']>row['SMA50']:
           print('Long')
           CASH,message=buy(6)
           print(message)
        elif row['SMA20']<row['SMA50'] and row['SMA20']<row['Close']:
            CASH,message=sell(7)
            print(message)
        elif row['SMA20']<row['SMA50']:
            print('Short')
            CASH,message=sell(2)
            print(message)

            

def on_tick(symbol):
    aapl_data=OHLCV(symbol.upper(),"2013-01-01","2016-01-01")['history']['day']
    data = pd.DataFrame(aapl_data)
    while intraday_status()['clock']['state']=='closed':  
        analysis(data)


def buy(quantity):
    for x in get_quotes('AAPL'):
        current_ask_price=x['ask']
        CASH=0
        CASH=FUNDS-(current_ask_price*quantity)
        return CASH,'Your Funds after this order: {}'.format(CASH)

def sell(quantity):
    for x in get_quotes('AAPL'):
        CASH=0
        current_ask_price=x['ask']
        CASH=FUNDS+(current_ask_price*quantity)
        return CASH,'Your Funds after this order: {}'.format(CASH)
    



on_tick('AAPL')



