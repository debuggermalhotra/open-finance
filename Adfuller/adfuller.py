from wrapper import *
from kloudtrader.equities.data import close_prices
from kloudtrader.defaults import ACCESS_TOKEN,ACCOUNT_NUMBER
import statsmodels.tsa.stattools as ts
import pandas as pd

data=close_prices('AMZN','2000-01-01','2015-01-01')
amzn=pd.DataFrame(data)

#Preforming Augmented Dickey-Fuller test for Amazon
ts.adfuller(amzn,1)