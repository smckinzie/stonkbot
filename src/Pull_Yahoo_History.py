


import pandas_datareader
import datetime


stonk = 'PSLV'

def get_ytd(stonk):
    tod = datetime.datetime.now()
    d = datetime.timedelta(days = 20)
    a = str(tod - d)
    start_list = a.split()
    start = start_list[0] 
    print(a)
    yahoo_ytd = pandas_datareader.data.DataReader(name=stonk, data_source='yahoo', start=start)
    print(yahoo_ytd)
    return yahoo_ytd

pslv = get_ytd(stonk)
print(pslv)