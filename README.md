# EMA-50 Market Efficiency and Forecasting Bot

### An Econometric & Algorithmic Investigation of FX Market Predictability

This repository presents a dual-track investigation into the market efficiency of the **CHF/JPY** currency pair. It integrates a Python-based algorithmic trading system with a rigorous **Applied Econometrics** audit to determine if EMA-based technical signals possess statistically significant predictive power or if the market follows a Random Walk.

---

## 👨‍💻 About the Project

Unlike standard trading bots that rely solely on backtesting, this project subjects its signals to formal hypothesis testing. It contrasts the **practical ROI** of a trading algorithm against the **theoretical constraints** of the Efficient Market Hypothesis (EMH).

### Core Research Question
*Does the 50-period Exponential Moving Average (EMA-50) contain embedded information that can statistically forecast future log-returns, or are the returns a "Fair Game" process as defined by Fama (1970)?*

---

## 📂 Repository Contents

| File Name | Description | Key Econometric Concepts |
| :--- | :--- | :--- |
| `Econometric_Validation_Report.pdf` | Full academic paper auditing the strategy's predictive power. | **Weak-form EMH**, **Stationarity (ADF/KPSS)**, **AR(1) Processes**, **Predictive Regression**. |
| `Project_Hypothesis_and_Methodology.pdf` | Operational framework and hypothesis formulation. | **Random Walk Hypothesis**, **Volatility Clustering**, **Look-ahead Bias**, **Lagged Covariance**. |
| `trading_bot.py` *(example)* | The execution algorithm. | **Pattern Recognition**, **Risk Management**, **EMA Crossovers**. |

---

## 📊 Econometric Methodology

To validate the "scientific" legitimacy of the trading signals, I applied the following econometric diagnostics (detailed in `Econometric_Validation_Report.pdf`):

### 1. Stationarity & Random Walk Tests
Financial time series often exhibit non-stationary behavior (unit roots). I validated the data properties using:
* **Augmented Dickey-Fuller (ADF) Test:** Used to reject the Null Hypothesis of a unit root in log-returns ($p < 0.01$).
* **KPSS Test:** Used to confirm stationarity around a deterministic trend.
* *Result:* Prices ($P_t$) follow a Random Walk, while Returns ($r_t$) are stationary.

### 2. Serial Correlation (Memory) Analysis
I tested for market "memory" (inefficiency) using:
* **Autocorrelation Function (ACF):** To detect if past returns ($r_{t-k}$) influence current returns.
* **AR(1) Regression:** Modeled as $r_t = \alpha + \phi r_{t-1} + u_t$ to estimate the persistence coefficient $\phi$.
* **Durbin-Watson Statistic:** To detect autocorrelation in the residuals of the predictive model.

### 3. Predictive Power Evaluation
A formal regression analysis was conducted:
$$r_{t+1} = \beta_0 + \beta_1 \cdot \text{Signal}_t + \epsilon_{t+1}$$
* **Objective:** Determine if the $\beta_1$ coefficient for the EMA-Signal is statistically significantly different from zero.

---

## 🤖 Algorithmic Implementation

While the econometric audit tests for *statistical* significance, the bot tests for *economic* significance (profitability after costs).

* **Signal Logic:** Uses a confluence of EMA-50 trend filtering and Candlestick Pattern Recognition (Doji, High-Wave).
* **Risk Optimization:** Incorporates volatility indices to dynamically adjust position sizing, reducing downside drawdown by ~11%.
* **Performance:** The backtesting engine (built with `Backtesting.py`) suggests a forecast precision improvement of 5–8% in specific volatility regimes, despite the high efficiency of the broader market.

---

## 🛠 Technical Stack & Libraries

* **Econometrics:** `Statsmodels` (ADF, OLS regression), `SciPy`
* **Data Science:** `Pandas`, `NumPy`, `Matplotlib` (Visualization)
* **Trading:** `MetaTrader 5 API` (Data sourcing), `Backtesting.py`

---

## 📜 Citation

If you use the methodology or code from this repository, please cite the enclosed research:

> **Tulanov, D. (2025).** *Technical Analysis, Market Efficiency, and the Predictive Power of EMA-50 in the CHFJPY Foreign Exchange Market.* Seoul National University, Department of Economics.
