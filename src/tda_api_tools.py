# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 13:40:26 2020

@author: Yung
"""
import requests
import pandas as pd
import json
import os
import sys
from datetime import datetime
sys.path.append('../')


#API Keys
file = open("../tdam_secret.json") # REPLACE YOUR API KEY HERE
keys = json.load(file)["key"]


def get_price_history(symbol:str, **kwargs) -> str:
    """

    Parameters
    ----------
    symbol : str
        DESCRIPTION.
    **kwargs : TYPE
        keyword arguments MUST match api call parameters

    Returns
    -------
    Pandas DataFrame of API Call

    """
    try:
        #initialize base_url and request parameters
        base_url = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(symbol) #base url and format with input string
        payload={"apikey": keys} #define/initiate search  param

        for key, values in kwargs.items(): #update kwargs
            if key == "startDate" or key=="endDate":
                values = datetime_to_unix(values)
            payload[key] = values
        # get requests
        content = requests.get(url=base_url, params=payload) #get item content
        
        if content.json()["empty"]:
            print("Empty Response")
            return pd.DataFrame()
        else:
            return apiout_to_df(content.json())
    except ValueError:
        print("Check Value Formats")
        
def datetime_to_unix(time:str):
    """

    Parameters
    ----------
    time : str
        Time in YYYY-MM-DD HH:MM:SS format

    Returns
    -------
    UNIX time converted from datetime

    """
    dates = pd.to_datetime(time)
    check_time = (dates - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
    return str(check_time)+"000"

def apiout_to_df(apiout:dict)->pd.DataFrame:
    out_df = pd.DataFrame(apiout["candles"])
    out_df["to_datetime"] = out_df.datetime.apply(lambda x: int(str(x)[:-3]))
    out_df.to_datetime = out_df.to_datetime.apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S.%f"))
    out_df.datetime = out_df.to_datetime
    out_df.index = pd.DatetimeIndex(out_df.datetime)
    out_df.drop(["datetime", "to_datetime"], inplace=True, axis=1)
    return out_df

def get_latest_history(symbol, frequency=1, frequencyType="minute"): 
    end = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") # end date of the data collection 
    import_df = get_price_history(symbol,
                      period=1, 
                      periodType="day",
                      frequency=5,
                      frequencyType="minute",
                      endDate=end)
    output_df = pd.DataFrame()

    while len(import_df.index) > 1:
        print("importing from ", end)
        import_df = get_price_history(symbol, 
                          frequency=frequency,
                          frequencyType=frequencyType, 
                          endDate=end)
        if len(import_df.index) > 0:
            end = import_df.index[0]
            output_df = pd.concat([import_df, output_df])
            print("sucessfully imported on ", end)
        else:
            print("check last import date")
            break

    print(f"Imported Data from {symbol}")
    print("from {}".format(output_df.index[0]))
    print("to {}".format(output_df.index[-1]))
    return output_df