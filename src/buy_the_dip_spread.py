### Import libraries
import pprint as pp
import time
import random
import sys
import TDAPI
import importlib
from datetime import datetime

arg = sys.argv
if len(arg) < 5:
    print('Arguments Required: Stonk Ticker, Test or Prod, Buy Start Percentage, Sell Start Percentage')
    exit()
elif arg[2].lower() == 'test':
    loop_time = 5
    is_prod = False
elif arg[2].lower() == 'prod':
    loop_time = 29
    is_prod = True
else:
    print('Arguments Required: Stonk Ticker, Test or Prod, Buy Start Percentage, Sell Start Percentage')
    exit()

####### Stonk we be trading ##########
stonk = arg[1].upper()
######################################
try:
    file = open("/home/shawn/TDAmeritrade/" + stonk + "_count.py", "x")
    file.write("total_profit = 0.0 \n" + "total_shares = 0")
    file.close()
except:
    print('file already exsists')

### Main function      
def main():
########### Trading Varsiables #############
    start_buy_percent = float(arg[3]) / 100
    start_buy_percent_multi = 0.01
    start_sell_percent = float(arg[4]) / 100
    start_sell_percent_multi = 0.01
    share_count = 0
##############################################
    stonk_var = importlib.import_module("%s_count" % stonk)
    total_profit = stonk_var.total_profit
    total_shares = stonk_var.total_shares
    print('<<<<<<<<<<>>>>>>>>>> {} <<<<<<<<<<>>>>>>>>>>'.format(stonk))
    endtime = random.randint(1933,1956)   

### Try to Login and Pull API data once every minute for 60 minutes  
    for i in range(60):
        try:
            TDSession = TDAPI.td_login()
            close_list_five = TDAPI.get_close_list(TDSession,stonk,5,10)
            close_list_one = TDAPI.get_close_list(TDSession,stonk,1,1)
            sma_one = sum(close_list_one) / len(close_list_one)
            sma_five = sum(close_list_five) / len(close_list_five)
            quote = TDAPI.get_price(TDSession,stonk) 
            base_price = quote[stonk]['lastPrice']          
            break
        except Exception as e:
            print('###########TDA API FAILURE#########')
            print(e)
            print(i)
            print('###########TDA API FAILURE#########')
            time.sleep(60)
            pass
# Set the base share counts for buying and selling
    sell_diff = base_price - sma_five
    buy_diff = sma_five - base_price
    if base_price > 13:
        buy_count = 1
        sell_count = 1  
    elif base_price < 1:
        buy_count = 10
        sell_count = 10          
    else:
        buy_count = int(13 // base_price)
        sell_count = int(13 // base_price)
    print(buy_count)
    print(sell_count)
    print(base_price)
    share_limit = 35 * buy_count
    margin_limit = -35 * sell_count    
    if buy_diff <= 0:
        today_buy_threshold = 0.0
    else:
        today_buy_threshold = buy_diff / sma_five

    if sell_diff <= 0:
        today_sell_threshold = 0.0
    else:
        today_sell_threshold = sell_diff / sma_five
    
    print('Daily Buy threshold percent: {}'.format(today_buy_threshold))
    print('Daily Sell threshold percent: {}'.format(today_sell_threshold))
    buy_percent = start_buy_percent
    sell_percent = start_sell_percent
    buy_percent_multi = start_buy_percent_multi
    sell_percent_multi = start_sell_percent_multi
### Random Start Delay
    if is_prod == True:
        r = random.randint(3,56)
        print('Delayed start of {} seconds'.format(r))
        time.sleep(r)

### Loop that checks stock prices every 5 minutes, appends price to rolling average, and cycles 168 times 
    for i in range(2000):
        print('<<<<<<<<<<>>>>>>>>>> {} <<<<<<<<<<>>>>>>>>>>'.format(stonk))
        try:
            quote = TDAPI.get_price(TDSession,stonk)
            last_price = quote[stonk]['lastPrice']
            close_list_one.pop(0)
            close_list_one.append(last_price)
            sma_one = sum(close_list_one) / len(close_list_one)
            print('{} five day simple moving average: {}'.format(stonk,sma_five)) 
            print('{} Rolling one day simple moving average: {}'.format(stonk,sma_one)) 
            hour = datetime.now().hour * 100
            minute = datetime.now().minute
            now = hour + minute

        except Exception as e:
            print('###########TDA API FAILURE#########')
            print(e)
            print(i)
            time.sleep(60)
            print('###########TDA API FAILURE#########')
            pass

        total_buy_threshold = (1 - (today_buy_threshold + buy_percent)) * sma_five
        total_sell_threshold = (1 + (today_sell_threshold + sell_percent)) * sma_five
        if share_count + buy_count > share_limit:
            print('share count over daily share limit')
            exit()
        elif share_count - sell_count < margin_limit:
            print('share count over daily margin limit')
            exit()
        elif is_prod == True and now >= endtime:
            print('End of Day Exit')
            exit()
        else:
            try:
                last_price = quote[stonk]['lastPrice']
                ask_price = quote[stonk]['askPrice']
                bid_price = quote[stonk]['bidPrice']
                print('Current ask price of {}: {}'.format(stonk,ask_price))
                print('Current last price of {}: {}'.format(stonk,last_price))
                print('Current bid price of {}: {}'.format(stonk,bid_price))
                if ask_price < total_buy_threshold and ask_price < sma_one:
                    #ask_price = ask_price * 0.999
                    ask_price = float(f'{ask_price:.2f}')
                    print('Buy {} {} for {} per share'.format(buy_count,stonk,ask_price))
                    share_count += buy_count
                    total_shares += buy_count
                    total_profit -= ask_price * buy_count
                    today_sell_threshold = 0.0                     
                    if is_prod == True:
                        TDAPI.buy_stock(TDSession,stonk,ask_price,buy_count)
                        time.sleep(240)
                    buy_percent_multi *= 1.5
                    buy_percent += buy_percent_multi
                    sell_percent = start_sell_percent
                    sell_percent_multi = start_sell_percent_multi        
                    buy_count *= 2
                    file = open("/home/shawn/TDAmeritrade/" + stonk + "_count.py", "w")
                    file.write("total_profit = " + str(total_profit) + "\n" + "total_shares = " + str(total_shares))
                    file.close()

                elif bid_price > total_sell_threshold and bid_price > sma_one:
                    #bid_price = bid_price * 1.001
                    bid_price = float(f'{bid_price:.2f}')
                    print('Sell {} {} for {} per share'.format(sell_count,stonk,bid_price))
                    share_count -= sell_count
                    total_shares -= sell_count
                    total_profit += bid_price * sell_count
                    today_buy_threshold = 0.0 
                    if is_prod == True:
                        TDAPI.sell_stock(TDSession,stonk,bid_price,sell_count)
                        inverse_buy_price = (bid_price * 0.95)
                        inverse_buy_price = float(f'{inverse_buy_price:.2f}')
                        if sell_count == 1:
                            inverse_buy_count = 1
                        else:
                            inverse_buy_count = sell_count // 2
                        duration = 'DAY'
                        time.sleep(240)
                        TDAPI.buy_stock(TDSession,stonk,inverse_buy_price,inverse_buy_count,duration)
                    
                    sell_percent_multi *= 1.5
                    sell_percent += sell_percent_multi  
                    buy_percent = start_buy_percent
                    buy_percent_multi = start_buy_percent_multi                   
                    sell_count *= 2
                    file = open("/home/shawn/TDAmeritrade/" + stonk + "_count.py", "w")
                    file.write("total_profit = " + str(total_profit) + "\n" + "total_shares = " + str(total_shares))
                    file.close()
                else:
                    print('hodl {}'.format(stonk))
                quote = TDAPI.get_price(TDSession,stonk)
            except Exception as e:
                print('###########TDA API FAILURE#########')
                print(e)
                print(i)
                time.sleep(60)
                print('###########TDA API FAILURE#########')
                pass
        print('total buy percent: {}  total buy threshold: {}'.format(today_buy_threshold + buy_percent,total_buy_threshold))
        print('total sell percent: {}  total sell threshold: {}'.format(today_sell_threshold + sell_percent,total_sell_threshold)) 
        print('{} Daily share count: {}'.format(stonk,share_count))
        print('Total Trade Cash Value: {}'.format(total_profit))
        print('Total Share Count: {}'.format(total_shares))
        time.sleep(loop_time)
    print('Done')

### Run the main function    
if __name__ == "__main__":
    main()