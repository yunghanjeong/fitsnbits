# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 19:34:37 2021

@author: Yung
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error



class arima_tools():
    def __init__(self):
        self._ = ""
    
    
    def moving_averages(self, input_df, days_list:list = [10, 50], col:str="close"):
        """
        This function returns a dataframe output_df with specified col and its moving averages per specified by days_list
        
        Input
        ========
        input_df: Pandas DatafFrame of stock prices. It is recommended that index is datetime and the columns contain "open, high, low, and close"
        
        days_list: list of integers to create moving averages. DEFAULT = [10, 50]
        
        col: name of the columns to create MA from the input_df. This must be part of input_df.columns. DEFAULT = "close"
        
        Output
        ========
        output_df: A pandas dataframe with specified col and its moving averages per specified by days_list
        """    
        
        output_df = input_df.copy() # to not disturb original data
        out_ma_columns = [col] #intial lize output column list with input column
    
        for day in days_list:
            column = f"MA({day})"
            output_df[column] = output_df[col].rolling(day).mean() #make rolling/moving averages
            out_ma_columns.append(column) #build output column list
        
        return output_df[out_ma_columns].dropna() #output df with no errors

    def differences (self, input_df, nlags=5, find_least=True):
        """
        This function returns a dataframe output_df with lags of all columns on dataframe specified by orders of lags.
        
        Input
        ========
        input_df: Pandas DatafFrame of stock prices. It is recommended that index is datetime and the columns contain "open, high, low, and close"
        
        lags: # of lags DEFAULT = 1
        
        Output
        ========
        output_df: A pandas dataframe with lags of all columns
        
        """
        output_df = input_df.copy() #to not disturb input data
        input_columns = output_df.columns
        
        # for all lags
        for i in range(1, nlags+1):
            current_lag_columns = []
            for col in input_columns:
                col_name = "{}_lag_{}".format(col, i)
                current_lag_columns.append(col_name)
        
                output_df[col_name] = output_df[col].diff(i)
            
            if find_least:
                for col in current_lag_columns:
                    stationarity = self.adf_test(output_df[col])["reject null hypothesis"]
                    if stationarity:
                        zip(col, i)
                        
    
        return output_df.dropna()
    
    def adf_test(self, timeseries:pd.Series, lags="AIC", alpha=0.05):
        """
        This function returns a dataframe output_df with specified col and its moving averages per specified by days_list
        
        Input
        ========
        input_df: Pandas DatafFrame of stock prices. It is recommended that index is datetime and the columns contain "open, high, low, and close"
        
        days_list: list of integers to create moving averages. DEFAULT = [10, 50]
        
        col: name of the columns to create MA from the input_df. This must be part of input_df.columns. DEFAULT = "close"
        
        Output
        ========
        output_df: A pandas dataframe with specified col and its moving averages per specified by days_list
        
        """
        
        dftest = adfuller(timeseries, autolag=lags) #adf_result of this time series
        dfoutput = pd.Series([timeseries.name], index=["series name"]) #get inputname
        dfoutput = pd.concat([dfoutput, pd.Series(dftest[0:4], index=["Test Statistic", 
                                                                      "p-value", 
                                                                      "#Lags Used", 
                                                                      "Number of Observations Used"])]) #get adf result values
        
        #================Reject Null Hypothesis based on p-value and alpha==========================#
        # data has potential to be stationary if this is true
        if dfoutput["p-value"] <= alpha:
            dfoutput["reject null hypothesis"] = True
        else:
            dfoutput["reject null hypothesis"] = False
        
        
        
        for key,value in dftest[4].items():
            dfoutput["Critical Value (%s)"%key] = value #add critical value
            
        return dfoutput
    
    def find_lag_stationary(self, input_df, nlags=5):
        org_cols = input_df.columns()
        test_df = input_df.copy()
     
        