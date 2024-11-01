import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import mplfinance as mpf
import matplotlib.pyplot as plt
import talib.abstract as ta

from . import tconfig as tc
buy_color = tc.kbuy
sell_color = tc.ksell
average_color = tc.kavg
base_color = tc.kbase
band_color = tc.kband
kcolor = tc.kline
dcolor = tc.dline

def initial_input(df):
    # Unify numeric type to float
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].astype(float)
    # Make sure 'ts' as index
    if 'ts' in df.columns:
        df['timestamp'] = pd.to_datetime(df.ts)
        df.set_index('timestamp', inplace=True) 
    else:
        df['timestamp'] = pd.to_datetime(df.date)
        df.set_index('timestamp', inplace=True) 
    # mpl need 'volume' column
    if 'vol' in df.columns:
        df['volume'] = df.vol
    return df

def ta_convert(df):
    # Convert to TA-Lib format
    if 'Open' in df.columns:
        df['open'] = df.Open
    if 'High' in df.columns:
        df['high'] = df.High
    if 'Low' in df.columns:
        df['low'] = df.Low
    if 'Close' in df.columns:
        df['close'] = df.Close
    if 'Volume' in df.columns:  
        df['volume'] = df.Volume
    if 'vol' in df.columns:
        df['volume'] = df.vol
    
    return df

def get_style(select = 1, color_up = buy_color, color_down = sell_color):
    color_up = buy_color
    color_down = sell_color
    marketcolors = mpf.make_marketcolors(up=color_up,down=color_down, inherit=True)
    #mpf.available_styles()
    switch = {
        1: mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=marketcolors),
        2: mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=marketcolors),
        3: mpf.make_mpf_style(base_mpf_style='starsandstripes', marketcolors=marketcolors),
        4: mpf.make_mpf_style(base_mpf_style='tradingview', marketcolors=marketcolors)

    }   
    return switch[select]

def get_addplot(df, select = 1):

    df = ta_convert(df)
    # 計算布林通道
    bbands = ta.BBANDS(df, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)

    # 計算KD指標
    kd = ta.STOCH(df, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    # 計算MACD
    macd = ta.MACD(df, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_diff = macd['macd'] - macd['macdsignal']
    macd_diff_pos = np.where(macd_diff > 0, macd_diff, np.nan)  # 正值
    macd_diff_neg = np.where(macd_diff < 0, macd_diff, np.nan)  # 負值

    # 添加指標作為附圖
    apds = [
        mpf.make_addplot(bbands['upperband'], color=band_color, linestyle='--', width=0.75),
        mpf.make_addplot(bbands['middleband'], color=average_color, linestyle='-', width=0.75),
        mpf.make_addplot(bbands['lowerband'], color=band_color, linestyle='--', width=0.75),
        mpf.make_addplot(kd['slowk'], panel=2, color=kcolor, ylabel='KD', y_on_right=True),
        mpf.make_addplot(kd['slowd'], panel=2, color=dcolor),
        #mpf.make_addplot(macd['macd'] - macd['macdsignal'], panel=3, color='m', type='bar', width=0.75,ylabel='MACD', y_on_right=True)
        mpf.make_addplot(macd_diff_pos, type='bar', panel=3, color=buy_color, width=0.75, ylabel='MACD', y_on_right=True),
        mpf.make_addplot(macd_diff_neg, type='bar', panel=3, color=sell_color, width=0.75)
    ]

    return apds

def ts_slice(df, s_slice= "08:40:00", e_slice = "10:00:00"):

    if 'date' in df.columns:
        date = df.date.iloc[0]
    elif 'ts' in df.columns:
        ts = pd.to_datetime(df.ts.iloc[0])
        date = ts.strftime("%Y-%m-%d")

    df = df[df['ts'] >= f"{date} {s_slice}"]
    df = df[df['ts'] <= f"{date} {e_slice}"]

    return df

def change_to_n_kbars(df, n = 5):
    df = initial_input(df)

    df = ta_convert(df)
    
    if 'date' in df.columns:
        df['date'] = df['date'].resample(f'{n}T').first()

    df['open'] = df['open'].resample(f'{n}T').first()
    df['high'] = df['high'].resample(f'{n}T').max()
    df['low'] = df['low'].resample(f'{n}T').min()
    df['close'] = df['close'].resample(f'{n}T').last()
    df['volume'] = df['volume'].resample(f'{n}T').sum()
    df = df.dropna()
    return df

# This is basic kbars plot function
def kbar(df, style = None):
    
    df = initial_input(df)
    
    if style is None:
        style = get_style(1)

    mpf.plot(df, 
         title='K-Bar',
         type='candle',
         style=style,
         volume=True,
         figsize=(14, 8),
         warn_too_much_data=1000
        )  

# This is singe day for minute kbars plot function
def mkbar(df, style = None, addplot = None, filename = 'mkbars', show = False):
    
    df = initial_input(df)

    end_time = df.index[-1]
    start_time = df.index[0]
    print(f"start_time: {start_time}, end_time: {end_time}")

    if addplot is None:
        df = ta_convert(df)
        bbands = ta.BBANDS(df, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
        addplot = [mpf.make_addplot(bbands['upperband'], linestyle='--', color=band_color),
                   mpf.make_addplot(bbands['middleband'], linestyle='-', color=average_color),
                   mpf.make_addplot(bbands['lowerband'], linestyle='--', color=band_color)]
    if style is None:
        style = get_style(1)

    if show == False:
        output_path = './imgs/' + filename + '.jpg'
        output_dict = dict(fname=output_path, dpi=200)
        mpf.plot(df, 
            title=filename,
            type= 'candle', #'ohlc'
            addplot=addplot,
            xlim=(pd.to_datetime(start_time), end_time),
            style=style,
            savefig=output_dict,
            volume=True,
            figsize=(14, 8),
            figscale=1.0, 
            panel_ratios=(5, 1),
            warn_too_much_data=2000
        )  
    else:
        mpf.plot(df, 
            title=filename,
            type= 'candle', #'ohlc'
            addplot=addplot,
            xlim=(pd.to_datetime(start_time), pd.to_datetime(end_time)),
            style=style,
            volume=True,
            figsize=(14, 8),
            figscale=1.0, 
            panel_ratios=(5, 1),
            warn_too_much_data=2000
        )  

# This daily kbars plot function
def dkbar(df, style = None, addplot = None, filename = 'dkbars.png', show = False):
    
    df = initial_input(df)

    if addplot is None:
        df = ta_convert(df)
        bbands = ta.BBANDS(df, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
        addplot = [mpf.make_addplot(bbands['upperband'], linestyle='--', color = band_color),
                   mpf.make_addplot(bbands['middleband'], linestyle='-', color = average_color),
                   mpf.make_addplot(bbands['lowerband'], linestyle='--', color = band_color)]
    if style is None:
        style = get_style(1)

    start_time  = df.index[0]
    end_time = df.index[-1]

    output_path = './imgs/' + filename + '.jpg'
    output_dict = dict(fname=output_path, dpi=100)
    if show == False:
        mpf.plot(df, 
            title=filename,
            type= 'candle', #'ohlc'
            addplot=addplot,
            xlim=(pd.to_datetime(start_time), pd.to_datetime(end_time)),
            style=style,
            savefig=output_dict,
            volume=True,
            figsize=(14, 8),
            figscale=1.0, 
            panel_ratios=(5, 1),
            warn_too_much_data=2000
        )  
    else:
        mpf.plot(df, 
            title=filename,
            type= 'candle', #'ohlc'
            addplot=addplot,
            xlim=(pd.to_datetime(start_time), pd.to_datetime(end_time)),
            style=style,
            volume=True,
            figsize=(14, 8),
            figscale=1.0, 
            panel_ratios=(5, 1),
            warn_too_much_data=2000
        )  

