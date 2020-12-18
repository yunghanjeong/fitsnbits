# FitsnBits

FitsnBits is a stock market prediction models that allows the investors to make a data driven decisions. The model 

## Overview

## Methods

## Data Collection

## ARIMA Selection (ACF and PACF)

![s&p500](https://github.com/yunghanjeong/fitsnbits/blob/main/images/SPY.acf_pacf.png?raw=true)

## Model

## Results

### BEST
![s&p500](https://github.com/yunghanjeong/fitsnbits/blob/main/images/V_prediction.png?raw=true)
![JPM](https://github.com/yunghanjeong/fitsnbits/blob/main/images/JPM_prediction.png?raw=true)
![VISA](https://github.com/yunghanjeong/fitsnbits/blob/main/images/SPY_prediction.png?raw=true)

### WORST

## Repository Structure
```
├── README.md                       # Top-level README
├── fitsnbits.ipynb                 # Narrative documentation of the project in Jupyter Notebook
├── fitsnbits_presentation.pdf      # PDF version of project presentation
├── src                             # Contains custom python modules
│   └── tda_api_tools.py            # Query tool for TD Ameritrade
├── images                          # All plots and visualization of project
├── notebooks                       # Noteboooks used to build the project
│   └── tdameritrade_api.py         # TD Ameritrade API Calls and data collection
│   └── spy_stocks_eda.py           # EDA of collected data
│   └── tdameritrade_api.py         # TD Ameritrade API Calls and data collection
├── models                          # Saved models
└── data                            # Data obtained from TD Ameritrade API Calls
```