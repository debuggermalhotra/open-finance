from time import sleep
import pandas as pd
from kloudtrader.equities.data import *
from kloudtrader.alert_me import email
from kloudtrader.defaults import PT_ACCESS_TOKEN,PT_ACCOUNT_NUMBER
from kloudtrader.equities.papertrade import *

def hello():
    for x in get_quotes('AAPL'):
        yield x['ask']

for x in hello():
    print('original {}'.format(x))
    print('added {}'.format(float(x)+2))
    sleep(3)

