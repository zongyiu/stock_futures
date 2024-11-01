import pandas as pd
import exchange_calendars 
from datetime import datetime


exlusive_date = ["2021-02-08", "2021-02-09", "2021-04-02", "2021-04-30",  "2022-01-27", "2022-02-04", "2023-08-03", "2024-02-06", "2024-02-07", "2024-07-24", "2024-07-25", "2024-10-02", "2024-10-03"]    

add_date = ["2024-09-16"]

def get_trading_day_list(start, end):

    start_check = pd.to_datetime(start)
    end_check = pd.to_datetime(end)
    
    if start_check > end_check:
        return None

    #twtc = trading_calendars.get_calendar('XTAI')
    twtc = exchange_calendars.get_calendar('XTAI')

    dates = pd.date_range(start,end)
    
    day_list = []

    for date in dates:
        date = date.strftime("%Y-%m-%d")
        if date in twtc.opens or date in add_date:             
            if not date in exlusive_date: 
                day_list.append(date)

    return day_list


def get_previous_trading_day(date, num = 1):

    twtc = exchange_calendars.get_calendar('XTAI')

    date = pd.to_datetime(date)
    for i in range(num):
        check = False
        while not check:
            p1date = date - pd.Timedelta(days=1)
            _pdate = p1date.strftime("%Y-%m-%d")
            if _pdate in twtc.opens or _pdate in add_date:
                check = True
            else:
                date = p1date
        date = p1date
        pdate = date

    pdate = pdate.strftime("%Y-%m-%d")
    
    if pdate in exlusive_date:
        return get_previous_trading_day(pdate)

    return pdate

def get_latest_trading_day():

    twtc = exchange_calendars.get_calendar('XTAI')

    date = datetime.now().strftime("%Y-%m-%d")

    if check_trading_date(date):
        return date
    
    else:    
        return get_previous_trading_day(date)



def check_trading_date(date):

    twtc = exchange_calendars.get_calendar('XTAI')

    if (date in twtc.opens and not (date in exlusive_date)) or (date in add_date):
        return True
    else:
        return False
