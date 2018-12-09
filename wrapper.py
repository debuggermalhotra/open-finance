from requests import *
from time import sleep

API_URL="http://127.0.0.1:5000/"

def get_all_quotes():
    response=get(API_URL+"quotes")
    try:
        return response.json()
    except:
        raise ("Did not recieve any data. Status Code: {}".format(response.status_code))

def get_quotes(symbol):
    response=get(API_URL+"quotes/"+symbol)
    try:
        return response.json()
    except:
        raise ("Did not recieve any data. Status Code: {}".format(response.status_code))

def get_all_trades():
    response=get(API_URL+"trades/")
    try:
        return response.json()
    except:
        raise ("Did not recieve any data. Status Code: {}".format(response.status_code))

def get_trades(symbol):
    response=get(API_URL+"trades/"+symbol)
    try:
        return response.json()
    except:
        raise ("Did not recieve any data. Status Code: {}".format(response.status_code))




def get_ask_prices(symbol):
    response=get(API_URL+"quotes/"+symbol)
    try:
        import numpy as np
        from numpy_ringbuffer import RingBuffer
        from time import sleep
        r = RingBuffer(capacity=4,dtype=float)
        for x in response.json():
            r.append(x['ask'])
            np.array(r)
            return np.array(r)
    except:
        raise ("Did not recieve any data. Status Code: {}".format(response.status_code))