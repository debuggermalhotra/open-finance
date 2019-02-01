#Mean Reversion Strategy in Python
from kloudtrader.defaults import *
from kloudtrader.equities.data import close_prices
from kloudtrader.user import account_positions,account_balance
from kloudtrader.alert_me import *
import datetime
import pandas as pd
import ta

def analysis(symbol):
    close_data=close_prices(symbol,'2018-01-01',datetime.date.today())
    df=pd.DataFrame(close_data)
    window=15
    df['EMA']=ta.trend.ema_indicator(df['close'],n=window)
    df['long_entry_point']=df['EMA']-(5/100)*df['EMA']
    df['sell_entry_point']=df['EMA']+(5/100)*df['EMA']
    df=df.iloc[window:]
    df['Buy']=df.apply(lambda x : 1 if x['close']<x['EMA'] else 0,axis=1)
    df['Sell']=df.apply(lambda x : 1 if x['close']>x['EMA'] else 0,axis=1)
    return df

def trade(symbol):
    
    today=str(datetime.date.today())
    data=analysis(symbol.upper())
    data=data.loc[data['date']==today]
    if data['Buy'].item()==1:
        while data['close'].item()<data['long_entry_point'].item() and account_balance()['balances']['total_cash']>=2000:
            buy(5,symbol)
            print('Long')
            message="Mean-Reversion algo had a Long Signal and 5 of {} will be bought if cash is more than $2000".format(symbol)
            email('chetan@kloudtrader.com',message)
    elif data['Sell'].item()==1:
        # Calculating the number of positions we hold for the given stock
        my_positions=account_positions()
        for k,v in my_positions.items():
            if v['position']['symbol']==symbol:
                symbol_position_qantity=v['position']['quantity']
        while data['close']>data['sell_entry_point'] and symbol_position_qantity>=0:
            sell(2,symbol)
            print('Sell')
            message="Mean-Reversion algo had a Sell Signal, position will be closed for {}".format(symbol)
            email('chetan@kloudtrader.com',message)
                
while intraday_status()['clock']['state']!='closed':
    trade('AAPL')