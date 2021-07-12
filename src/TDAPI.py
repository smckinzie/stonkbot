### Import libraries
from td.client import TDClient
import numpy as np
import pandas as pd

### Create a new session
def td_login():
    TDSession = TDClient(
        client_id='XXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        redirect_uri='https://127.0.0.1',
        credentials_path='/home/shawn/TDAmeritrade/CREDENTIALS_FILE'
    )
### Login to the session
    TDSession.login()
    return TDSession

### Grab 5 Day Average 
def get_rolling(TDSession,stonk,value):
    rolling_list = []
    history = TDSession.get_price_history(symbol=stonk,period=5,period_type='day',frequency=30,frequency_type='minute')
    history = history.get('candles')
    for item in history:
            rolling_list.append(item.get(value))
    rolling_average = sum(rolling_list) / len(rolling_list)
    return rolling_average


### Grab 10 Day average 
def get_average(TDSession,stonk):
    stonk_list = []
    history = TDSession.get_price_history(symbol=stonk,period=5,period_type='day',frequency=30,frequency_type='minute')
    history = history.get('candles')
    for item in history:
        if len(stonk_list) < 480:
            stonk_list.append(item.get('close'))
        else:
            stonk_list.pop(0)
            stonk_list.append(item.get('close'))     
    stonk_average = sum(stonk_list) / len(stonk_list) 
    return stonk_average 

### Grab One day average
def get_fivemin_rolling(TDSession,stonk):
    rolling_list = []
    history = TDSession.get_price_history(symbol=stonk,period=1,period_type='day',frequency=5,frequency_type='minute')
    history = history.get('candles')
    for item in history:
        if len(rolling_list) < 100:
            rolling_list.append(item.get('close'))
        else:
            rolling_list.pop(0)
            rolling_list.append(item.get('close'))
    return rolling_list

### Grab real-time quotes for Stonk
def get_price(TDSession,stonk):
    quote = TDSession.get_quotes(instruments=[stonk])
    return quote

### Buy Stock
def buy_stock(TDSession,stonk,price,buy_count):
    print('BUY {}'.format(stonk))
    order_dict = {
        "session": "SEAMLESS",
        "duration": "GOOD_TILL_CANCEL",
        "orderType": "LIMIT",
        "quantity": buy_count,
        "price": price,
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "orderLegType": "EQUITY",
            "instrument": {
                "assetType": "EQUITY",
                "symbol": stonk
                },
            "instruction": "BUY",
            "quantity": buy_count,
            "quantityType": "SHARES"
            }
        ],
    }
    TDSession.place_order(account='XXXXXXXXX',order=order_dict)

### Sell Stock
def sell_stock(TDSession,stonk,price,sell_count):
    print('SELL {}'.format(stonk))
    order_dict = {
        "session": "SEAMLESS",
        "duration": "GOOD_TILL_CANCEL",
        "orderType": "LIMIT",
        "quantity": sell_count,
        "price": price,
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "orderLegType": "EQUITY",
            "instrument": {
                "assetType": "EQUITY",
                "symbol": stonk
                },
            "instruction": "SELL",
            "quantity": sell_count,
            "quantityType": "SHARES"
            }
        ],
    }
    TDSession.place_order(account='XXXXXXXXX',order=order_dict)

############################################################################
### Buy Stock via Stop Limit Order
def buy_stop_limit(TDSession,stonk,price,best_price,buy_count):
    print('BUY {}'.format(stonk))
    order_dict = {
        "session": "NORMAL",
        "duration": "DAY",
        "orderType": "STOP_LIMIT",
        "quantity": buy_count,
        "stopPrice": price,
        "price": best_price,
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "orderLegType": "EQUITY",
            "instrument": {
                "assetType": "EQUITY",
                "symbol": stonk
                },
            "instruction": "BUY",
            "quantity": buy_count,
            "quantityType": "SHARES"
            }
        ],
    }
    TDSession.place_order(account='XXXXXXXXXX',order=order_dict)

### Sell Stock via Stop Limit Order
def sell_stop_limit(TDSession,stonk,price,best_price,sell_count):
    print('SELL {}'.format(stonk))
    order_dict = {
        "session": "NORMAL",
        "duration": "DAY",
        "orderType": "STOP_LIMIT",
        "quantity": sell_count,
        "stopPrice": price,
        "price": best_price,
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "orderLegType": "EQUITY",
            "instrument": {
                "assetType": "EQUITY",
                "symbol": stonk
                },
            "instruction": "SELL",
            "quantity": sell_count,
            "quantityType": "SHARES"
            }
        ],
    }
    TDSession.place_order(account='XXXXXXXXXX',order=order_dict)


### Buy Stock via Trailing Stop Limit Order
def buy_trail_stop(TDSession,stonk,buy_count):
    print('BUY {}'.format(stonk))
    order_dict = {
        "session": "NORMAL",
        "duration": "GOOD_TILL_CANCEL",
        "orderType": "TRAILING_STOP",
        "quantity": buy_count,
        "stopPriceLinkBasis": "LAST",
        "stopPriceLinkType": "PERCENT",
        "stopPriceOffset": 2,
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "orderLegType": "EQUITY",
            "instrument": {
                "assetType": "EQUITY",
                "symbol": stonk
                },
            "instruction": "BUY",
            "quantity": buy_count,
            "quantityType": "SHARES"
            }
        ],
    }
    TDSession.place_order(account='XXXXXXXXXX',order=order_dict)

### Sell Stock via Trailing Stop Limit Order
def sell_trail_stop(TDSession,stonk,sell_count):
    print('BUY {}'.format(stonk))
    order_dict = {
        "session": "NORMAL",
        "duration": "GOOD_TILL_CANCEL",
        "orderType": "TRAILING_STOP",
        "quantity": sell_count,
        "stopPriceLinkBasis": "LAST",
        "stopPriceLinkType": "PERCENT",
        "stopPriceOffset": 2,
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "orderLegType": "EQUITY",
            "instrument": {
                "assetType": "EQUITY",
                "symbol": stonk
                },
            "instruction": "SELL",
            "quantity": sell_count,
            "quantityType": "SHARES"
            }
        ],
    }
    TDSession.place_order(account='XXXXXXXXXX',order=order_dict)

    ### Grab 5 Day Price List 
def get_close_list(TDSession,stonk,period=5,frequency=30):
    close_list = []
    history = TDSession.get_price_history(symbol=stonk,period=period,period_type='day',frequency=frequency,frequency_type='minute')
    history = history.get('candles')
    for item in history:
            close_list.append(item.get('close'))
    return close_list

def get_ratio_list(stonk1_list,stonk2_list):
    ratio_list = []
    for i in range(0,len(stonk2_list)-1):
        ratio_list.append(stonk1_list[i] / stonk2_list[i])
    return ratio_list

#######################################################################


def get_ema(prices,smoothing=2):
    ema = [prices[0]]
    n = 1
    x = 0
    for price in range(1,len(prices)):
        n += 1
        x += 1
        ema.append(prices[x] * (smoothing / (1 + n)) + prices[x-1] * (1 - (smoothing / (1 + n))))
    print(len(ema))
    return ema

