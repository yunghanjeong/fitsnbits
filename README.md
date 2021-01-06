# FitsnBits
![banner](https://github.com/yunghanjeong/fitsnbits/blob/main/images/banner_fidelity.png?raw=true)
Fitsnbits is a stock position potential indicator based on moving average crossover trading strategy. Any traders with access to [TD Ameritrade API](https://developer.tdameritrade.com/apis) can utilize this project to research a new position or update their current account standings. Moving average crossovers are the point when a stock price cross overs it's moving average prices which can provide strong signals to buy or sell. This project will predict daily closing and moving average prices of a given stock and calculate its crossover potential to assist market strategies. 


## Business Case
A recent article by LPL Financial on [Websteronline](https://public.websteronline.com/articles/investments-insights/how-different-generations-invest) demonstrated the stark difference in new and young investors compared to established older generation. The young investors tends to rely on individual research intuition and invest with shorter goals in mind, but older investors relied on professional advisors and brokers to grow their portfolio. This investment pattern was also confirmed by [Wall Street Journal](https://www.wsj.com/articles/the-baby-boomer-vs-millennial-investment-smackdown-11559813581) where young investors are more likely to invest in emerging companies and IPOs to boos their porfolio. 

There is a clear market gap between providing a reliable and economical financial quantitative tool for younger and emerging indepedent investors. This project aims to provide a simplified and modular tool set for any indepedent investors who are looking to explore the market individually.

## Overview
 The data for the prediction was collected using [TD Ameritrade API](https://developer.tdameritrade.com/apis) with support of pandas, numpy, and datetime library of Python. S&P500 (SPY) Index and the **Big 10** companies of the index: Apple, Microsoft, Amazon, Facebook, Google (Class A & C), Berkshire Hathaway, Johnson & Johnson, JPMorgan Chase, and Visa was chosen as the focus group of the prototype of this project. The **Big 10** companies take up more than quarter of the total index in performance and was found that they behaved and trended similarly to S&P500s. For prediction modeling ARIMA was performed on daily closing prices of the selected stock prices with the ARIMA orders being determined by results of partial autocorrelation and gridsearch of each individual stocks with root-mean-squared-error as the error metric. 

## Methods
1. Historic stock quotes were collected from selected companies through TD Ameritrade API between 2018-2020
2. Moving Average Calculated as additional indicator
3. ARIMA order for daily close price were calculated
    - Augmented Dickey-Fuller
    - Autocorrelation Partial Autocorrelation
4. ARIMA model built and tested


## Data 
### EDA
The collected data from TD Ameritrade API is very clean and free of null values as expected. The data has datetime index with open, close, high, and low prices along with its daily total trade volume. For this analysis only the close prices will be looked at since we assume that a trade strategy would be made in advance. 

In summary, both all companies chosen for this project behaved similarly in 2020:

- COVID-19 Market crash cause very quick crash in stock values
 - Moving average crossovers only resulted in resistance due to the crash
- Recovery turned mostly positive by end of the year
- Recovery was steady
 - Moving average crossovers started to signal support
    
### 2020 Performance

#### S&P500
S&P500 index is one of the known reliable investment that turns profit in consistent intervals. The year 2020 was similar even with the large COVID-19 Market crash highlighted below. The upward trend, minus the crash, indicates that linear regression might be a good fit for baseline analysis. 

Note the concentration of longer candlesticks (price ranges) during the crash period compared to recovery and growth that occur after the crash. 

![spy2020candlestick](https://github.com/yunghanjeong/fitsnbits/blob/main/images/spy_2020_candlestick.png?raw=true)

#### Big 10
Repeating the analysis above for S&P500 on the Big 10 stock mentioned above tells very similar story. All companies suffered unprecedent crash during COVID-19 market crash. Hoewever, most companies still managed to end the year with positive growth. Majority of the company saw stready recovery after the crash except for JNJ, which saw a very quick recovery. AAPL, AMZN, and GOOGL behaved very similarly to S&P500. JPM was the biggest outlier in both recovery and trend.

![aapl2020candlestick](https://github.com/yunghanjeong/fitsnbits/blob/main/images/aapl_2020_candlestick.png?raw=true)

![jpm2020candlestick](https://github.com/yunghanjeong/fitsnbits/blob/main/images/jpm_2020_candlestick.png?raw=true)


Moving average crossovers showed resistance during the crash, which is to be expected. As S&P500 did, these companies crossovers started to signal suppport in recovering months after the crash. 

#### Moving Average and Monthly Breakdown
![monthlybreadkwon](https://github.com/yunghanjeong/fitsnbits/blob/main/images/SPY_2020_monthly.png?raw=true)


## Model
The model will be built with **ARIMA** (AutoRegressive Integrated Moving Average) model and will be tested on predicting the last 2 weeks of trading in 2020 with stock prices so far. The strategy is following:


1. Split data for forward propagation testing
    - predict last 2 weeks of trading in 2020, note only 8 days of trading due to end of the year. 
2. Create a baseline model
    - Linear Regression
3. Calculate best ARIMA starting point
    - Stationarity
    - ACF and PACF
4. Compare each model perforamnce
    - RMSE
5. Predict and compare model perforamnce

### Baseline
A linear regression model was built as a baseline for comparing the model performance. As emphasized before, the COVID-19 crash added a lot of dynamic in stock price in 2020 and generalized model like linear regression performed poorly. It's prediction error (RMSE) was 134.3 which over 35% of the true values. 

![linear_regresion](https://github.com/yunghanjeong/fitsnbits/blob/main/images/spy_linear_fit.png?raw=true)

### ARIMA
To prepare the ARIMA model for forecasting on our data few parameters must be caluclated and analyzed. First and foremost, the input data must be stationary for **AR** and **MA** models. The stationarity can be checked with Augmented Dickey-Fuller test.  Then, autocorrelation and partial autocorrelation functions (ACF andACF) can be utilized to calculated the **AR** and **MA** orders.

#### Stationarity and ADF

The dynamic nature of the current data set is a clear indication of non-stationarity within our data. ADF test on the data also fails reject the null hypothesis. However taking a difference of lag 1 shows stationarity. Visualization of difference at first lag also shows relative stationarity. 

Most stocks data gather in project marked stationarity at `d=1` for ARIMA starting point.

![stationarity_spy](https://github.com/yunghanjeong/fitsnbits/blob/main/images/spy_lag_1.png?raw=true)

#### ACF and PACF 

Autocorrelation (ACF) and Partical Autocorrelation functions (PACF) are used to determine the order of **AR** and **MA** (p, q) in ARIMA model. Both functions check for level of significance each lag that contributes to the true value. ACF can provide significance in lag order for both **AR** and **MA** models. PACF are particularly useful in determining **AR** (p) order of the ARIMA model. 

Visualized ACF and PACF of closing price and moving averages are below. In each price columns the ACF results indicates significant correlation in each lag indicating non-stationarity. PACF result for each price columns indicated that `p = 2` is a good candidate for the ARIMA model. 

![acf_pacf_spy](https://github.com/yunghanjeong/fitsnbits/blob/main/images/SPY.acf_pacf.png?raw=true)

#### Building ARIMA
Fitting ARIMA models orders of (2, 1, 1) and (2, 1, 2) on `S&P500`resulted in much closer prediction in true value than linear regression. Given the importance of stationarity of ARIAM model the rolling averages should be predicted by ARIMA in similar fashion and most likely require the same ARIMA order.

Overall, ARIMA of (2, 1, 1) performed best with: 
- RMSE: 2.47
- %RMSE: 0.0066
- Model assumed steady, but in reality the stock increased
    - decrease from most recent lag likely have large impact on prediction

![arima_211_spy](https://github.com/yunghanjeong/fitsnbits/blob/main/images/spy_arima_211_pred.png?raw=true)

ARIMA of (2, 1, 2) had a very close performance. 

![arima_212_spy](https://github.com/yunghanjeong/fitsnbits/blob/main/images/spy_arima_212_pred.png?raw=true)

###### Prediction on Moving Averages
The model prediction was close to the real value, but failed capture the upward trend of real data. However, the market position potential still could be calculating by predicting the moving average with same logic and seeing their total comparitive behavior. 

In summary:

- ARIMA model perform very well in predicting moving average
    - Support from utilzing average as data
    - Very low RMSE
- Crossover analysis for S&P500 indicates good buying position
    - Indication for potential buy at 12-21 through 12-23 
    - ~2% gain until end of year

![arima_211_ma_spy](https://github.com/yunghanjeong/fitsnbits/blob/main/images/spy_MA_arima_pred.png?raw=true)  

## Results

Extending the method above to all other stock analysis resulted in ARIMA order in favor of (2, 1, 1). It was found that (2, 0, 0) was best fit for Johnson and Johnson and (2, 1, 0) was best firt for JPMorgan Chase and Visa, which was also affirms the behavioral difference noticed in visual exploreration. In predicting with moving average the prediction on JNJ, GOOGL, GOOG, and JPM were more accurate. 

JNJ prediction showed merging potential between price prediction and moving average, which indicates upcoming crossover points. Choosing to invest in this period in JNJ would result in profit. 

![arima_211_ma_jnj](https://github.com/yunghanjeong/fitsnbits/blob/main/images/JNJ_MA_arima_pred.png?raw=true)  


## Conclusion
Overall, all prediction made in this project yielded good insights to market entrance using ARIMA to predict moving average crossover points in S&P500 and its top 10 stocks. Trading year 2020 had market movements, especially with COVID-19 crash, which makes modeling based on this time period very different. Traditional linear regression was demonstrated early on how poor it can be in predicting wiht overall data due to its sensitivity with outliers. Utilizing ARIMA method seeks to avoid issues by relying prediction on lag based observation. The ARIMA method was proven effective with:

- Fast calculation and implementation
- Low RMSE
- Statistical test based order selection

### Future Works

- Create Ensemble with regression and ARIMA
- forward propagate in smaller resolution
- Streamline process for less end-user programming
- Deploy application or library of final model for ease of use
- Deploy plotly tools for dashboard building


## Repository Structure
```
├── README.md                           # Top-level README
├── fitsnbits.ipynb                     # Narrative documentation of the project in Jupyter Notebook
├── fitsnbits_presentation.pdf          # PDF version of project presentation
├── src                                 # Contains custom python modules
│   └── tda_api_tools.py                # Query tool for TD Ameritrade
├── images                              # All visualization and images of the project
├── notebooks                           # Noteboooks used to build the project
│   └── tdameritrade_api.ipynb          # TD Ameritrade API Calls and data collection
│   └── spy_stocks_eda.ipynb            # EDA of collected data
│   └── tdameritrade_api.ipynb          # TD Ameritrade API Calls and data collection
│   └── arima_eda_class.ipynb           # ARIMA Builder OOP Notebook
├── models                              # Saved models
└── data                                # Data obtained from TD Ameritrade API Calls
```