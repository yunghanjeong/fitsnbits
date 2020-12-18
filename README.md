# FitsnBit
FitsnBits is a stock market prediction models that allows the investors to make a data driven decisions by simplifying time series analysis process. A recent article by LPL Financial on [Websteronline](https://public.websteronline.com/articles/investments-insights/how-different-generations-invest) demonstrated the stark difference in new and young investors compared to established older generation. The young investors tends to rely on individual research intuition and invest with shorter goals in mind, but older investors relied on professional advisors and brokers to grow their portfolio. This investment pattern was also confirmed by [Wall Street Journal](https://www.wsj.com/articles/the-baby-boomer-vs-millennial-investment-smackdown-11559813581) where young investors are more likely to invest in emerging companies and IPOs to boos their porfolio. 

Given the lack of free/open-source resources 

## Overview
![banner]()

FitsnBits is a stock market prediction models that allows the investors to make a data driven decisions by simplifying time series analysis process. The data for the prediction was collected using [TD Ameritrade API](https://developer.tdameritrade.com/apis) with support of pandas, numpy, and datetime library of Python. S&P500 (SPY) Index and the **Big 10** companies of the index: Apple, Microsoft, Amazon, Facebook, Google (Class A & C), Berkshire Hathaway, Johnson & Johnson, JPMorgan Chase, and Visa was chosen as the focus group of the prototype of this project. It was found that the 11 selected stock prices behaved and trended similarly, which streamlined the EDA And modeling process. For prediction modeling ARIMA was performed on daily closing prices of the selected stock prices with the ARIMA orders being determined by results of partial autocorrelation and gridsearch of each individual stocks with root-mean-squared-error as the error metric. Overall, it was found that AR (2) was the common starting point of the gridsearch hypertuning of all models with all models performing within 3% of %RMSE of their respective stock prices. 

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
├── images                          # All visualization and images of the project
├── notebooks                       # Noteboooks used to build the project
│   └── tdameritrade_api.py         # TD Ameritrade API Calls and data collection
│   └── spy_stocks_eda.py           # EDA of collected data
│   └── tdameritrade_api.py         # TD Ameritrade API Calls and data collection
├── models                          # Saved models
└── data                            # Data obtained from TD Ameritrade API Calls
```