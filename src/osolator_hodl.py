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
    print('Arguments Required: Stonk Ticker, Test or Prod, Buy Count, Sell Count')
    exit()
elif arg[2].lower() == 'test':
    loop_time = 5
    is_prod = False
elif arg[2].lower() == 'prod':
    loop_time = 29
    is_prod = True
else:
    print('Arguments Required: Stonk Ticker, Test or Prod, Buy Count, Sell Count')
    exit()

####### Stonk we be trading ##########
stonk = arg[1].upper()
######################################

try:
    file = open("/home/shawn/TDAmeritrade/hodl_" + stonk + "_state.py", "x")
    file.write("total_profit = 0.0 \n" + "round_trip_up = 0 \n" + "round_trip_down = 0 \n" + "got_stonk = False")
    file.close()
except:
    print('file already exsists')

### Main function      
def main():
########### Trading Varsiables #############
    buy_count = int(arg[3])
    sell_count = int(arg[4])
    share_limit = 85
    margin_limit = -85
    share_count = 0
    oso_low = 0
    oso_high = 0
##############################################
    stonk_var = importlib.import_module("hodl_%s_state" % stonk)
    total_profit = stonk_var.total_profit
    round_trip_up = stonk_var.round_trip_up
    round_trip_down = stonk_var.round_trip_down
    got_stonk = stonk_var.got_stonk
    print('<<<<<<<<<<>>>>>>>>>> {} <<<<<<<<<<>>>>>>>>>>'.format(stonk))
    endtime = random.randint(1633,1656)
    starttime = 707
### Try to Login and Pull API data once every minute for 60 minutes  
    for i in range(60):
        try:
            TDSession = TDAPI.td_login()
            close_list_one = TDAPI.get_close_list(TDSession,stonk,1,1)
            sma_one = sum(close_list_one) / len(close_list_one)     
            quote = TDAPI.get_price(TDSession,stonk)
            print(quote)
            ask_price = quote[stonk]['askPrice']
            bid_price = quote[stonk]['bidPrice']
            bot_ask_price = ask_price
            bot_bid_price = bid_price
            fast_list = [ask_price] * 26
            slow_list = [ask_price] * 96
            #slow_list = close_list_one[-96:]
            oso_list = [0] * 3
            crossover_pad = ask_price * 0.005
            reverse_pad = ask_price * 0.001
            break
        except Exception as e:
            print('###########TDA API FAILURE#########')
            print(e)
            print(i)
            print('###########TDA API FAILURE#########')
            time.sleep(60)
            pass

### Random Start Delay
    if is_prod == True:
        r = random.randint(3,56)
        print('Delayed start of {} seconds'.format(r))
        time.sleep(r)

### Loop that checks stock prices every 1 minute, appends price to rolling average, and cycles 1000 times 
    for i in range(2000):
        print('<<<<<<<<<<>>>>>>>>>> {} <<<<<<<<<<>>>>>>>>>>'.format(stonk))
        try:
            sma_one = sum(close_list_one) / len(close_list_one)
            print('{} Rolling one day simple moving average: {}'.format(stonk,sma_one)) 
            fast_average = sum(fast_list) / len(fast_list)
            print('{} Rolling fast price average: {}'.format(stonk,fast_average)) 
            slow_average = sum(slow_list) / len(slow_list)
            print('{} Rolling slow price average: {}'.format(stonk,slow_average)) 
            osolator = fast_average - slow_average
            print('{} Osolator: {}'.format(stonk,osolator)) 
            oso_average = sum(oso_list) / len(oso_list)
            print('{} Lowest Osolator Value of last cycle: {}'.format(stonk,oso_low)) 
            print('{} Highest Osolator Value of last cycle: {}'.format(stonk,oso_high)) 
            quote = TDAPI.get_price(TDSession,stonk)
            ask_price = quote[stonk]['askPrice']
            bid_price = quote[stonk]['bidPrice']
            close_list_one.pop(0)
            close_list_one.append(ask_price)
            fast_list.pop(0)
            fast_list.append(ask_price)
            slow_list.pop(0)
            slow_list.append(ask_price)
            oso_list.pop(0)
            oso_list.append(osolator)
            hour = datetime.now().hour * 100
            minute = datetime.now().minute
            now = hour + minute

        except Exception as e:
            print('###########TDA API FAILURE#########')
            print(e)
            print(i)
            print('###########TDA API FAILURE#########')
            pass

        if share_count + buy_count > share_limit:
            print('share count over daily share limit')
            exit()
        elif share_count - sell_count < margin_limit:
            print('share count over daily margin limit')
            exit()
        elif is_prod == True and now >= endtime:
            print('End of day exit')
            if got_stonk == True:
                print('Hodl Stock')
                exit()
            else:
                exit()

        else:
            try:
                print('Current ask price of {}: {}'.format(stonk,ask_price))
                print('Current bid price of {}: {}'.format(stonk,bid_price))
                if osolator < 0 + crossover_pad and osolator > 0 - crossover_pad:
                    print('Do nothing until out of crossover zone')
                    time.sleep(loop_time)
                elif now <= starttime and now <= endtime - 200:
                    print('Do nothing prior to start time')
                    time.sleep(loop_time)
                elif got_stonk == False:
                    if osolator < 0 - crossover_pad and osolator > oso_low + reverse_pad:
                        print("BUY!")
                        share_count += buy_count
                        total_profit -= ask_price * buy_count
                        if is_prod == True:
                            TDAPI.buy_stock(TDSession,stonk,ask_price,buy_count)
                        bot_ask_price = ask_price
                        bot_bid_price = bid_price
                        got_stonk = True
                        oso_low = 0
                        file = open("/home/shawn/TDAmeritrade/hodl_" + stonk + "_state.py", "w")
                        file.write("total_profit = " + str(total_profit) + "\n" + "round_trip_up = " + str(round_trip_up) + "\n" + "round_trip_down = " + str(round_trip_down) + "\n" + "got_stonk = True")
                        file.close()
                        time.sleep(loop_time) 
                    else:
                        print('Not time to buy {} yet'.format(stonk))
                        time.sleep(loop_time) 
                                           
                elif got_stonk == True:
                    if bid_price > bot_ask_price * 1.014 and osolator > 0 + crossover_pad and osolator < oso_high - reverse_pad:
                        print("SELL up 1.4 percent")
                        share_count -= sell_count
                        total_profit += bid_price * sell_count
                        if is_prod == True:
                            TDAPI.sell_stock(TDSession,stonk,bid_price,sell_count)
                        round_trip_up += 1
                        got_stonk = False
                        oso_high = 0
                        file = open("/home/shawn/TDAmeritrade/hodl_" + stonk + "_state.py", "w")
                        file.write("total_profit = " + str(total_profit) + "\n" + "round_trip_up = " + str(round_trip_up) + "\n" + "round_trip_down = " + str(round_trip_down) + "\n" + "got_stonk = False")
                        file.close()
                        time.sleep(loop_time)

                    else:
                        print("Not time to sell yet")
                        print('Bot Ask Price {}'.format(bot_ask_price))
                        print('Bot Bid Price {}'.format(bot_bid_price))
                        print('hodl {}'.format(stonk))
                        time.sleep(loop_time) 
                else:
                    print('Not time to sell {} yet'.format(stonk))
                    time.sleep(loop_time)  
                if osolator < 0 + crossover_pad and osolator > 0 - crossover_pad:
                    oso_high = 0
                    oso_low = 0                                             
                elif osolator < 0:
                    if osolator < oso_low:
                        oso_low = osolator
                    else:
                        print("Reverse UP!")
                elif osolator > 0:
                    if osolator > oso_high:
                        oso_high = osolator
                    else:
                        print("Reverse DOWN!")
                else:
                    print("NEVER")

            except Exception as e:
                print('###########TDA API FAILURE#########')
                print(e)
                print(i)
                print('###########TDA API FAILURE#########')
                pass
            time.sleep(loop_time)

        print('{} Got Stonk?: {}'.format(stonk,got_stonk))             
        print('{} Round Trip UP Count: {}'.format(stonk,round_trip_up))
        print('{} Round Trip DOWN Count: {}'.format(stonk,round_trip_down))
        print('{} Total Profit: {}'.format(stonk,total_profit))
    
    print('Done')

### Run the main function    
if __name__ == "__main__":
    main()