from time import sleep
import pandas as pd
from kloudtrader.equities.data import *
from kloudtrader.alert_me import email
from kloudtrader.defaults import ACCESS_TOKEN, ACCOUNT_NUMBER
import datetime
from collections import deque




df=pd.DataFrame()
def moving_avg():
        n=100
        d=deque(maxlen=n)
        for x in get_quotes('AAPL'): 
            d.appendleft(x['ask'])
            if len(d)==n:
                yield d
                d.pop()
            sleep(0.5)
              

for x in moving_avg():
        df['ask']=list(x)
        df['SMA']=df['ask'].rolling(window=15,center=False).mean()
        df['LMA']=df['ask'].rolling(window=25,center=False).mean()
        df['SMA2']=df['ask'].rolling(window=15,center=False).mean().shift(1)
        df['LMA2']=df['ask'].rolling(window=25,center=False).mean().shift(1)
        
        #df['Buy']=df.apply(lambda x : 1 if x['SMA']>x['LMA'] and x['SMA2']<x['LMA2'] else 0,axis=1)
        #df['Sell']=df.apply(lambda y : 1 if y['SMA']<y['LMA'] and y['SMA2']>y['LMA2'] else 0,axis=1)
        #df['Signal']=df['Buy']+df['Sell']
        for index,row in df.iterrows():
            if row['SMA']>row['LMA'] and row['SMA2']<row['LMA2']:
                if row['SMA']>row['ask']:
                    print('LONG signal at {}'.format(datetime.datetime.now()))
            if row['SMA']<row['LMA'] and row['SMA2']>row['LMA2']:
                if row['SMA']<row['ask']:
                    print("SHORT signal at {}".format(datetime.datetime.now()))
                
        '''
        for index,row in df.iterrows():
            if row['Buy']==1:
                print('Buy signal at: {}'.format(datetime.datetime.now()))
            elif row['Sell']==1:
                print('Sell signal at: {}'.format(datetime.datetime.now()))
                '''
        
        
       