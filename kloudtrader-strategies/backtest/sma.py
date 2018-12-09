from time import sleep
import pandas as pd
from kloudtrader.equities.data import *
from kloudtrader.alert_me import email
from kloudtrader.defaults import ACCESS_TOKEN, ACCOUNT_NUMBER


aapl_data=close_prices('AAPL',"2015-01-01","2016-01-01")
df=pd.DataFrame(aapl_data)
m=15
n=20
df['SMA']=df['close'].rolling(window=m,center=False).mean()
df['LMA']=df['close'].rolling(window=n,center=False).mean()
df['SMA2']=df['close'].rolling(window=m,center=False).mean().shift(1)
df['LMA2']=df['close'].rolling(window=n,center=False).mean().shift(1)
df=df.iloc[n:]
df['Buy']=df.apply(lambda x : 1 if x['SMA']>x['LMA'] and x['SMA2']<x['LMA2'] else 0,axis=1)
df['Sell']=df.apply(lambda y : 1 if y['SMA']<y['LMA'] and y['SMA2']>y['LMA2'] else 0,axis=1)
df['Signal']=df['Buy']+df['Sell']
df['Daily Returns']=df['close'].pct_change()
df['Strategy Returns']=df['Daily Returns']*df['Signal'].shift(1)
print(df)
