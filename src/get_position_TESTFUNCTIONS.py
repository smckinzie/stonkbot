### Import libraries
from td.client import TDClient
import pprint as pp
import time
import get_yahoo_historical

####### Stonk we be trading ##########
stonk = 'PHX'
######################################

### Create a new session
def td_login():
    TDSession = TDClient(
        client_id='5UXHQM8FAQHDXZI9GL8RIOF2RVXD8GCE',
        redirect_uri='https://127.0.0.1',
        credentials_path='/home/shawn/TDAmeritrade/CREDENTIALS_FILE'
    )
### Login to the session
    TDSession.login()
    return TDSession
### Grab real-time quotes for Stonk
def get_price(TDSession,stonk):
    quote = TDSession.get_quotes(instruments=[stonk])
    price = quote[stonk]['askPrice']
    return price


### Grab yesterday's Price  #NOT USED#
def get_24hour(TDSession,stonk,now):
    day1 = now - 86400000
    day2 = day1 - 60000
    print(now)
    print(day1)
    print(day2)
    hour24 = TDSession.get_price_history(symbol=stonk, start_date=day2)
    return hour24

### Grab real-time Account info #NOT USED#
def get_accounts(TDSession):
    accounts = TDSession.get_accounts(fields=['positions'])
    return accounts
    
### Grab Order info
def get_orders(TDSession):
    orders = TDSession.get_orders('425345821')
    return orders

### parce total stonk position value from acount info JSON
def pull_stonk_value(positions_all):
    for i in positions_all:
        if i['instrument']['symbol'] == stonk:
            stonk_value = i['marketValue']
    return stonk_value

### parce total stonk position count from acount info JSON
def pull_stonk_count(positions_all):
    for i in positions_all:
        if i['instrument']['symbol'] == stonk:
            stonk_count = i['longQuantity']
    return stonk_count

### Buy Stock
def buy_stock(TDSession,stonk,price,buy_count):
    print('SELL')
    print(stonk)
    #price = price + 0.01
    print(price)
    order_dict = {
        "session": "SEAMLESS",
        "duration": "DAY",
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
    TDSession.place_order(account='425345821',order=order_dict)

### Sell Stock
def sell_stock(TDSession,stonk,price,sell_count):
    print('SELL')
    print(stonk)
    #price = price - 0.01
    print(price)
    order_dict = {
        "session": "SEAMLESS",
        "duration": "DAY",
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
    TDSession.place_order(account='425345821',order=order_dict)
"""
### Main function      
def main():



### Run the main function    
if __name__ == "__main__":
    main()
"""
### TEST FUNCTIONS ###
TDSession = td_login()
accounts = get_accounts(TDSession)
positions_all = accounts[0]['securitiesAccount']['positions']
stonk_value = pull_stonk_value(positions_all)
stonk_count = pull_stonk_count(positions_all)
print(stonk_value)
print(stonk_count)
#chain = TDSession.get_options_chain(option_chain=stonk)
#print(chain)
stonk_intel = TDSession.get_instruments(cusip='654902204')
pp.pprint(stonk_intel)

#orders = get_orders(TDSession)
#pp.pprint(orders)
#now = int(time.time()) * 1000
#hour24 = get_24hour(TDSession,stonk,now)
#pp.pprint(hour24)

#price = get_price(TDSession,stonk)
#buy_stock(TDSession,stonk,price)
