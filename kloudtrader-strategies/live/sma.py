from kloudtrader.equities.data import * 
from collections import deque
import pandas as pd
from kloudtrader.defaults import ACCESS_TOKEN
import datetime
import itertool

df=pd.DataFrame()
short_window=2
long_window=4
askPriceBuffer_size=long_window+10
askPriceBuffer=deque(maxlen=askPriceBuffer_size)
SignalBuffer=deque(maxlen=25)


def live_feed_handler(symbol):    
    while len(askPriceBuffer)<=askPriceBuffer_size:
        live_ask_price=float(live_quotes(symbol.upper(),create_session())['ask'])
        askPriceBuffer.appendleft(live_ask_price)
        if len(askPriceBuffer)==askPriceBuffer_size:
            yield askPriceBuffer
            askPriceBuffer.pop()

for quotes in live_feed_handler('AAPL'):
    df['ask']=list(quotes)
    df['SMA']=df['ask'].rolling(window=short_window,center=False).mean()
    df['LMA']=df['ask'].rolling(window=long_window,center=False).mean()
    df['SMA2']=df['ask'].rolling(window=short_window,center=False).mean().shift(1)
    df['LMA2']=df['ask'].rolling(window=long_window,center=False).mean().shift(1)
    df['Buy']=df.apply(lambda x : 1 if x['SMA']>x['LMA'] and x['SMA2']<x['LMA2'] else 0,axis=1)
    df['Sell']=df.apply(lambda y : 1 if y['SMA']<y['LMA'] and y['SMA2']>y['LMA2'] else 0,axis=1)
    df['Signal']=df['Buy']+df['Sell']
    for index,row in df.iterrows():
        if row['SMA']>row['LMA'] and row['SMA2']<row['LMA2'] and row['SMA']>row['ask']:
            SignalBuffer.appendleft("LONG")
            
           
        elif row['SMA']<row['LMA'] and row['SMA2']>row['LMA2']and row['SMA']<row['ask']:
            SignalBuffer.appendleft("SHORT")
          

        if len(SignalBuffer)==SignalBuffer.maxlen:
            '''
            short_count=0
            long_count=0
            for ele in list(SignalBuffer): 
                if ele == "SHORT": 
                    short_count = short_count + 1
                elif ele == "LONG":
                    long_count = long_count + 1
            print("Long count {}".format(long_count)
            print("Short count {}".format(short_count))
            '''
            max(len(list(v)) for g,v in itertools.groupby(list(SignalBuffer)))
            SignalBuffer.pop()
             

                
            