EMA-50 Market Efficiency and Forecasting Bot

This repository presents an empirical and algorithmic investigation of the market efficiency and predictability of the CHF/JPY currency pair and selected assets from Forex and U.S. equities.
The study integrates econometric testing and data-driven trading algorithms to examine whether EMA-based signals carry statistically significant predictive power in financial markets.

Overview

The project implements data-driven trading strategies based on Exponential Moving Average (EMA) crossovers and candlestick pattern recognition, maintaining a consistent positive return on investment (ROI) across 4-hour and daily (1D) timeframes.
It also evaluates the econometric properties of these trading signals using formal statistical tests and incorporates portfolio-level risk controls.

Key Components
1. EMA-Based Trading Bot

A Python-based trading system was designed and backtested to evaluate the predictive performance of EMA crossovers.
The model improved forecast precision by 5–8%, achieved an overall 13% return, and automated risk-reward evaluation across multiple trading sessions.

2. Econometric Evaluation

The project investigates the CHF/JPY currency pair across multiple timeframes (H1, H4, D1, W1) using standard econometric diagnostics:

Augmented Dickey–Fuller (ADF) test for stationarity

Autocorrelation Function (ACF) for serial dependence

Durbin–Watson (DW) statistic for autocorrelation in residuals

These tests assess whether price returns follow a random walk and whether EMA-based signals capture inefficiencies.

3. Portfolio Risk Optimization

Volatility indices and drawdown limits were incorporated into portfolio management, reducing downside risk exposure by approximately 11% while maintaining the desired risk-adjusted performance.

Methodology

Data Collection
Historical OHLC data were obtained from MetaTrader 5 for multiple timeframes (H1–W1).

Signal Generation
EMA-50 crossover and candlestick confirmations were used to identify entry and exit points.

Backtesting
The strategy was evaluated in Python using Pandas, NumPy, and Matplotlib, focusing on ROI, Sharpe ratio, and drawdown analysis.

Econometric Testing
Statistical validation of the EMA-50 signal was conducted using Statsmodels (ADF, ACF, DW).

Results Summary
Metric	Result
Forecast Precision	+5 – 8 %
Total Return on Investment	13 %
Downside Risk Reduction	11 %
Timeframes Tested	H1, H4, D1, W1
Statistical Tests Used	ADF, ACF, Durbin–Watson
Technical Stack

Programming Language: Python

Libraries: Pandas, NumPy, Statsmodels, Matplotlib, Backtesting.py

Data Source: MetaTrader 5

Tools: Jupyter Notebook, Excel

Citation

Tulanov, D. (2025). EMA-50 Market Efficiency Analysis: An Econometric Evaluation of CHF/JPY Predictability.
