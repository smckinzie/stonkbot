### Import libraries
import pprint as pp
import time
import random
import sys
import TDAPI
import importlib
from datetime import datetime

####### Stonk we be trading ##########
stonk1 = 'SLV'
stonk2 = 'PSLV'
######################################


arg = sys.argv
if len(arg) < 2:
    print('Argument Required: Test or Prod')
    exit()
elif arg[1].lower() == 'test':
    loop_time = 5
    is_prod = False
elif arg[1].lower() == 'prod':
    loop_time = 59
    is_prod = True
else:
    print('Argument Required: Test or Prod')
    exit()

try:
    file = open("/home/shawn/TDAmeritrade/slv_and_pslv_count.py", "x")
    file.write("total_profit = 0.0 \n" + "slv_count = 100 \n" + "pslv_count = 300")
    file.close()
except:
    print('file already exsists')
### Main function      
def main():
########### Trading Varsiables #############
    stonk1_buy_count = 10
    stonk2_buy_count = 30
    stonk1_sell_count = 10
    stonk2_sell_count = 30
    start_slv_percent = 0.005
    start_slv_percent_multi = 0.005
    start_pslv_percent = 0.005
    start_pslv_percent_multi = 0.005
##############################################
    stonk_var = importlib.import_module("slv_and_pslv_count")
    total_profit = stonk_var.total_profit
    slv_count = stonk_var.slv_count
    pslv_count = stonk_var.pslv_count
    print('<<<<<<<<<<>>>>>>>>>> {} <<>> {} <<<<<<<<<<>>>>>>>>>>'.format(stonk1,stonk2))    
    TDSession = TDAPI.td_login()
    stonk1_ave = TDAPI.get_average(TDSession,stonk1)
    stonk2_ave = TDAPI.get_average(TDSession,stonk2)
    stonk_ratio = stonk1_ave / stonk2_ave
    print('Average Ratio of the two stonks: {}'.format(stonk_ratio))
### Try to Login and Pull API data once every minute for 60 minutes  
    for i in range(60):
        try:
            stonk1_list_five = TDAPI.get_close_list(TDSession,stonk1,5,5)
            stonk1_list_one = TDAPI.get_close_list(TDSession,stonk1,1,5)
            stonk2_list_five = TDAPI.get_close_list(TDSession,stonk2,5,5)
            stonk2_list_one = TDAPI.get_close_list(TDSession,stonk2,1,5)
            ratio_list_one = TDAPI.get_ratio_list(stonk1_list_one,stonk2_list_one)
            ratio_list_five = TDAPI.get_ratio_list(stonk1_list_five,stonk2_list_five)
            ratio_one = sum(ratio_list_one) / len(ratio_list_one)
            ratio_five = sum(ratio_list_five) / len(ratio_list_five)
            print('Ratio five average: {}'.format(ratio_one))
            print('Ratio one average: {}'.format(ratio_five))
            break
        except Exception as e:
            print('###########TDA API FAILURE#########')
            print(e)
            print(i)
            print('###########TDA API FAILURE#########')
            time.sleep(60)
            pass
    slv_percent = start_slv_percent
    slv_percent_multi = start_slv_percent_multi
    pslv_percent = start_pslv_percent
    pslv_percent_multi = start_pslv_percent_multi
    ### Loop that checks stock average every 5 minutes and cycles 280 times    
    while True:
        print('<<<<<<<<<<>>>>>>>>>> {} <<>> {} <<<<<<<<<<>>>>>>>>>>'.format(stonk1,stonk2))
        try:
            slv_pslv_threshold = (1 + slv_percent) * ratio_five
            pslv_slv_threshold = (1 - pslv_percent) * ratio_five
            print('Buy {} Sell {} Target Ratio: {}'.format(stonk2,stonk1,slv_pslv_threshold))
            print('Buy {} Sell {} Target Ratio: {}'.format(stonk1,stonk2,pslv_slv_threshold))
            stonk1_quote = TDAPI.get_price(TDSession,stonk1)
            stonk2_quote = TDAPI.get_price(TDSession,stonk2)
            stonk1_price = stonk1_quote[stonk1]['lastPrice']
            stonk2_price = stonk2_quote[stonk2]['lastPrice']
            #stonk1_price = float('24.' + str(random.randint(42,82)))
            #stonk2_price = float('9.' + str(random.randint(45,65)))
            print('Current price of {}: {}'.format(stonk1,stonk1_price))
            print('Current price of {}: {}'.format(stonk2,stonk2_price))
            current_ratio = stonk1_price / stonk2_price
            print('Current ratio of {} and {}: {}'.format(stonk1,stonk2,current_ratio))
            if current_ratio > ratio_five * (1 + pslv_percent):
                print('Buy {} Sell {}'.format(stonk2,stonk1))
                pslv_count += stonk2_buy_count
                slv_count -= stonk1_sell_count   
                pslv_percent_multi *= 1.5
                pslv_percent += pslv_percent_multi 
                slv_percent = start_slv_percent
                slv_percent_multi = start_slv_percent_multi           
                total_profit += (stonk2_price * stonk2_buy_count) - (stonk1_price * stonk1_sell_count)
                file = open("/home/shawn/TDAmeritrade/slv_and_pslv_count.py", "w")
                file.write("total_profit = " + str(total_profit) + "\n" + "slv_count = " + str(slv_count) + "\n" + "pslv_count = " + str(pslv_count))
                file.close()

            elif current_ratio < ratio_five * (1 - slv_percent) :
                print('Buy {} Sell {}'.format(stonk1,stonk2))
                pslv_count -= stonk2_sell_count
                slv_count += stonk1_buy_count  
                slv_percent_multi *= 1.5
                slv_percent += slv_percent_multi  
                pslv_percent = start_pslv_percent
                pslv_percent_multi = start_pslv_percent_multi
                total_profit += (stonk1_price * stonk1_buy_count) - (stonk2_price * stonk2_sell_count)
                file = open("/home/shawn/TDAmeritrade/slv_and_pslv_count.py", "w")
                file.write("total_profit = " + str(total_profit) + "\n" + "slv_count = " + str(slv_count) + "\n" + "pslv_count = " + str(pslv_count))
                file.close()
            else:
                print('hodl')
        except Exception as e:
            print('###########TDA API FAILURE#########')
            print(e)
            print('###########TDA API FAILURE#########')

        print('{} share count: {}'.format(stonk1,slv_count))
        print('{} share count: {}'.format(stonk2,pslv_count))       
        print('Trade profit: {}'.format(total_profit))
        time.sleep(loop_time)

### Run the main function    
if __name__ == "__main__":
    main()