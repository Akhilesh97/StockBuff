# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 21:03:26 2022

@author: Akhilesh
"""

import requests
import json
import datetime
import os
import pandas as pd

class extract_news:
    def __init__(self, api_key, ticker, from_date, to_date, filepath, base_url):
        self.api_key = api_key
        self.ticker = ticker
        self.from_date = from_date
        self.to_date = to_date
        self.base_url = base_url
        self.filepath = filepath
    
    def get_data(self):
        result = requests.get("%s?api_token=%s&s=%s&from=%s&to=%s&limit=1000"%(self.base_url, self.api_key, self.ticker, self.from_date, self.to_date))
        if result:
            print("Response - 200. Successful data extraction")
        else:
            print(result)
            print("API Limit Exceeded")
        return result
    
    def create_df(self, result):
        json_result = json.loads(result.text)
        df = pd.DataFrame.from_dict(json_result)
        return df
    
    def write_to_csv(self, df):
        print(self.filepath)
        if not os.path.exists(self.filepath):
            dirname = os.path.dirname(self.filepath)
            os.makedirs(dirname)
            
        df.to_csv(self.filepath)
        

def get_latest_news(ticker_):        
    api_key = "634b3c336bfff7.89514674"
    ticker = ticker_+".US"
    from_date =  str(datetime.datetime.today().year) + "-" +  str(datetime.datetime.today().month) + "-" + str(datetime.datetime.today().day-1)
    to_date  =  str(datetime.datetime.today().year) + "-" +  str(datetime.datetime.today().month) + "-" + str(datetime.datetime.today().day)
    current_date_str = str(datetime.date.today().month)+str(datetime.date.today().day)+str(datetime.date.today().year)
    filepath = "../data/%s/%s/%s_sentiment_data.csv"%(ticker.replace(".US",""), current_date_str, ticker.replace(".US","").lower())
    base_url = "https://eodhistoricaldata.com/api/news"
    
    extractor = extract_news(api_key, ticker, from_date, to_date, filepath, base_url)
    result = extractor.get_data()      
    df = extractor.create_df(result)
    extractor.write_to_csv(df)
    text = df["title"].values[-1]
    return text
    