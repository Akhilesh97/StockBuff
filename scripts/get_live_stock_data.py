# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 20:55:47 2022

@author: Akhilesh
"""

#Data Source
import yfinance as yf

def get_latest_stock_data(ticker):
    #Interval required 1 minute
    data = yf.download(tickers=ticker, period='2d', interval='1h')
    pre_latest_close = data["Close"].values[0]
    latest_close_price = data["Close"].values[-1]
    
    return round(latest_close_price,3), round(pre_latest_close,3)
