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

    def differences (self, input_df, nlags=1):
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

        for col in input_columns:
            for i in range(1, nlags+1):
                col_name = "{}_lag_{}".format(col, i)
                output_df[col_name] = output_df[col].diff(i)
        return output_df


    
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
    
    def find_lag_stationary(self, input_series, nlags=5):
        """

        Parameters
        ----------
        input_series : pd.Series 
            series to auto determine ARIMA lag d.
        nlags : int, optional
            number of lags to check up to . The default is 5.

        Returns
        -------
        TYPE
            first lag to be stationary with adf on differencing.

        """
        if self.adf_test(input_series)["reject null hypothesis"]:
           return 0
        for i in range (1, nlags+1):
            if self.adf_test(input_series.diff(i).dropna())["reject null hypothesis"]:
                break
        return i
        
    def get_pacf_lag(self, data, columns:list=["close"], nlags=20):
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
        lag_list = []
        for col in columns: # for specified columns
            # PACF significance and Results
            pacf_sig = 2/np.sqrt(len(data[col]))
            pacf_results = pacf(data[col], nlags=20)
            pacf_df = pd.DataFrame(pacf_results) 
            pacf_df.columns = ["sig"]
    
            # Differencing the significance to create keys for sorting by largest lag change
            pacf_df_diff = abs(pacf_df.sig.diff())
            pacf_df_diff.name = "sig_diff"
    
            # combine PACF results and differencing
            pacf_df = pd.concat([pacf_df, pacf_df_diff], axis=1)
            # filter out any data not shown significant
            pacf_df = pacf_df[abs(pacf_df.sig) > pacf_sig]
            # sort by the largest lag change
            pacf_df.sort_values(by="sig_diff", ascending=False, inplace=True)
            
            #store lag_list
            lag_list.append(pacf_df.index[0])
       #return a dataframe of results     
        return dict(zip(columns, lag_list))