# FitsnBit
![banner](https://github.com/yunghanjeong/fitsnbits/blob/main/images/banner_fidelity.png?raw=true)
FitsnBits is a stock market prediction models that allows the investors to make a data driven decisions by simplifying time series analysis process. A recent article by LPL Financial on [Websteronline](https://public.websteronline.com/articles/investments-insights/how-different-generations-invest) demonstrated the stark difference in new and young investors compared to established older generation. The young investors tends to rely on individual research intuition and invest with shorter goals in mind, but older investors relied on professional advisors and brokers to grow their portfolio. This investment pattern was also confirmed by [Wall Street Journal](https://www.wsj.com/articles/the-baby-boomer-vs-millennial-investment-smackdown-11559813581) where young investors are more likely to invest in emerging companies and IPOs to boos their porfolio. 

There is a clear market gap between providing a reliable and economical financial quantitative tool for younger and emerging indepedent investors. This project aims to provide a simple and efficient stock market analysis through streamlined ARIMA modeling for daily stock prices to forecast the next 5 days of stock prices. An accurate prediction from this model will allow each investors to predict their positions and accounts accordingly. 

## Overview

FitsnBits is a stock market prediction models that allows the investors to make a data driven decisions by simplifying time series analysis process. The data for the prediction was collected using [TD Ameritrade API](https://developer.tdameritrade.com/apis) with support of pandas, numpy, and datetime library of Python. S&P500 (SPY) Index and the **Big 10** companies of the index: Apple, Microsoft, Amazon, Facebook, Google (Class A & C), Berkshire Hathaway, Johnson & Johnson, JPMorgan Chase, and Visa was chosen as the focus group of the prototype of this project. It was found that the 11 selected stock prices behaved and trended similarly, which streamlined the EDA And modeling process. For prediction modeling ARIMA was performed on daily closing prices of the selected stock prices with the ARIMA orders being determined by results of partial autocorrelation and gridsearch of each individual stocks with root-mean-squared-error as the error metric. Overall, it was found that AR (2) was the common starting point of the gridsearch hypertuning of all models with all models performing within 3% of %RMSE of their respective stock prices. 

## Methods
1. Historic stock quotes were collected from selected companies through TD Ameritrade API between 2018-2020, exclusing the COVID-19 market crash.
2. The collected data was cleaned and stored as CSV using pandas and datetime libraries.
3. Autocorrelation and Partial Autocorelation (ACF and PACF) of individual stocks were calculated for base AR order of ARIMA.
4. GridSearch was performed on rest of ARIMA orders (I and MA) to find the orders that provided the least amount of error based on RMSE.
5. The optimal ARIMA orders were used to predict on daily prices on weekly ranges (5 days) with 25 days of data.
6. Overall RMSE was found for prediction evaluation.

## ARIMA Model Selection (ACF and PACF)
ACF and PACF of all selected stocks demonstrated very similar results where the ACF has steady drop over the lags and PACF having sharp drop after lag 2. This provides a starting point of the ARIMA model at AR order of 2. 

![s&p500](https://github.com/yunghanjeong/fitsnbits/blob/main/images/SPY.acf_pacf.png?raw=true)

Based on the starting point of AR(2), the rest of ARIMA orders were determined by gridsearch with RMSE as the metric. The order of I was limited to the max AR order minus 1 (1) and the order of MA was limited to the maximum order of AR (2). The gridsearch resulted in most models with ARIMA order of (2, 1, 1) with JPM ARIMA order of (2, 0, 2) and GOOGL ARIMA order fo (2, 0, 1).

## Results
Overall, all models predicted daily closing prices accurately with %RMSE ranging from 1.5-3% of respective stock prices. Below are the three best performing models, which are S&P500, JPMorgan Chase, and VISA. 

### BEST
![s&p500](https://github.com/yunghanjeong/fitsnbits/blob/main/images/V_prediction.png?raw=true)
![JPM](https://github.com/yunghanjeong/fitsnbits/blob/main/images/JPM_prediction.png?raw=true)
![VISA](https://github.com/yunghanjeong/fitsnbits/blob/main/images/SPY_prediction.png?raw=true)

However, there was some irregularities that significantly impacted this model. On Google class C stock (GOOG) the prediction overshot steep climbs and drops resulting in significant jumps in peaks and valleys. Johnson and Johnson (JNJ) behaved similarly with very promiment jumps between the peaks and the valleys of daily prices. 

### WORST
![GOOG](https://github.com/yunghanjeong/fitsnbits/blob/main/images/GOOG_prediction.png?raw=true)
![JNJ](https://github.com/yunghanjeong/fitsnbits/blob/main/images/JNJ_prediction.png?raw=true)

## Conclusion
Overall, all prediction made in this project yielded more than satisfactory results with all models performing very accurately in the long run. Further work is necessary to stabilize the models sudden drops, especially the inclusion of flash crash due to COVID-19 breakout. This can be tacked by inclusion of seasonality and exogenous variable (SARIMAX) and custom regression model built on neural net with RNN or LSTM layers for inclusion of model "memories".

## Future Works

- Create more stable model through inclusion of seasonality and exogenous variable (SARIMAX)
- Develop custom regression model through neural net
- Streamline process for less end-user programming
- Deploy application or library of final model for ease of use
- Stabilize the model and include COVID-19 crash. 

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