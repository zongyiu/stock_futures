import os
import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3 
from datetime import datetime
from datetime import timedelta
from . import tradingday 
begin_date = '2020-01-01'

def check_db(db_path = "./db/future_kbarsS.db"):
    _path = Path(db_path) 
    
    if not _path.is_file():
        print("Can't find db file")
        return False
    else:
        return True

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True  
    except ValueError:
        return False  

# Get First Date 
def get_first_day(db_path = "./db/future_kbars.db", table = 'kbars'):

    if not check_db(db_path):
        return None

    summary = db_path
    conn = sqlite3.connect(summary)

    sqlcmd = "SELECT * FROM " + table + " ORDER BY ts ASC LIMIT 10"
    df = pd.read_sql(sqlcmd, conn)
    df.ts = pd.to_datetime(df.ts)
    sort = df.sort_values(by = 'date', ascending=False, ignore_index=True)
    latest_date = sort.date[0]
    
    conn.close()    

    return latest_date

# Get Latest Date 
def get_latest_day(db_path = "./db/future_kbars.db", table = 'kbars'):

    if not check_db(db_path):
        return None

    summary = db_path
    conn = sqlite3.connect(summary)

    sqlcmd = "SELECT * FROM " + table + " ORDER BY ts DESC LIMIT 10"
    df = pd.read_sql(sqlcmd, conn)
    df.ts = pd.to_datetime(df.ts)
    sort = df.sort_values(by = 'date', ascending=False, ignore_index=True)
    latest_date = sort.date[0]
    
    conn.close()    

    return latest_date

# Get kbars by Date  
def get_daily_data(date, db_path = "./db/future_kbars.db", table = 'kbars'):

    if not check_db(db_path):
        return None

    if not is_valid_date(date):

        print(f"{date} is not a valid date, please input a valid date in the format of 'YYYY-MM-DD'")
        return None
    
    _path = Path(db_path) 
    
    if not _path.is_file():
        print("Can't find db file")
        return pd.DataFrame()
 
    conn = sqlite3.connect(db_path)
    sqlcmd = f"SELECT * FROM {table} WHERE date = '{date}'"
    df = pd.read_sql(sqlcmd, conn)
    
    conn.close()    

    return df


def normalize_dates(start_date: str, end_date: str) -> tuple:

    date_format = "%Y-%m-%d"
    start_dt = datetime.strptime(start_date, date_format)
    end_dt = datetime.strptime(end_date, date_format)

    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    end_dt += timedelta(days=1)

    new_start_date = start_dt.strftime(date_format)
    new_end_date = end_dt.strftime(date_format)

    return new_start_date, new_end_date


def get_daily_data_range(sdate, edate,  db_path = "./db/future_kbars.db", table = 'kbars'):

    if not check_db(db_path):
        return None

    if not is_valid_date(sdate) or not is_valid_date(edate):

        print(f"{sdate}/{edate} is not a valid date, please input a valid date in the format of 'YYYY-MM-DD'")
        return None
    
    sdate, edate = normalize_dates(sdate, edate)

    _path = Path(db_path) 
    
    if not _path.is_file():
        print("Can't find db file")
        return pd.DataFrame()

    #date = pd.to_datetime(date)        
    conn = sqlite3.connect(db_path)
    sqlcmd = f"SELECT * FROM {table} WHERE ts >= '{sdate} 08:00:00' and ts <= '{edate} 06:00:00'"
    df = pd.read_sql(sqlcmd, conn)
    
    conn.close()    

    return df

def get_previous_n_data_range(edate, num = 1, db_path = "./db/future_kbars.db", table = 'kbars'):

    if not check_db(db_path):
        return None

    if not is_valid_date(edate):
        print(f"{edate} is not a valid date, please input a valid date in the format of 'YYYY-MM-DD'")
        return None
    
    _path = Path(db_path) 
    
    if not _path.is_file():
        print("Can't find db file")
        return pd.DataFrame()

    sdate = tradingday.get_previous_trading_day(edate, num)

    df = get_daily_data_range(sdate, edate,  db_path, table)

    return df


def get_daily_kbars_with_n_data_range(edate, num = 1, db_path = "./db/future_kbars.db", table = 'kbars'):
    
    df =  get_previous_n_data_range(edate, num , db_path, table)

    

