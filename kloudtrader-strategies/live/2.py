from kloudtrader.equities.data import * 
from collections import deque
import pandas as pd
from kloudtrader.defaults import ACCESS_TOKEN

df=pd.DataFrame()
short_window=10
long_window=20
askPriceBuffer_size=long_window+50


def handle_live_feed(symbol):
        live_ask_price=float(live_quotes(symbol.upper(),create_session(access_token="2HU89u9ikIX64eUcgrWqYaNEuxcS"))['ask'])
        return live_ask_price


def add_to_buffer():
    live_ask_price=handle_live_feed("AAPL")
    
    print(askPriceBuffer)
    while intraday_status()['clock']['state']!="closed":
        askPriceBuffer.append(live_ask_price)
        if len(askPriceBuffer)==askPriceBuffer_size:
            yield askPriceBuffer
            askPriceBuffer.pop()
    


for x in add_to_buffer():
    df['ask']=list(x)
    df['SMA']=df['ask'].rolling(window=short_window,center=False).mean()
    df['LMA']=df['ask'].rolling(window=long_window,center=False).mean()
    df['SMA2']=df['ask'].rolling(window=short_window,center=False).mean().shift(1)
    df['LMA2']=df['ask'].rolling(window=long_window,center=False).mean().shift(1)
    df['Buy']=df.apply(lambda x : 1 if x['SMA']>x['LMA'] and x['SMA2']<x['LMA2'] else 0,axis=1)
    df['Sell']=df.apply(lambda y : 1 if y['SMA']<y['LMA'] and y['SMA2']>y['LMA2'] else 0,axis=1)
    df['Signal']=df['Buy']+df['Sell']
    print(df)
    for index,row in df.iterrows():
        if row['SMA']>row['LMA'] and row['SMA2']<row['LMA2']:
            if row['SMA']>row['ask']:
                print('LONG signal at {}'.format(datetime.datetime.now()))
        if row['SMA']<row['LMA'] and row['SMA2']>row['LMA2']:
            if row['SMA']<row['ask']:
                print("SHORT signal at {}".format(datetime.datetime.now()))
    
