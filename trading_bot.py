import pandas as pd
import numpy as np
import datetime
import MetaTrader5 as mt5
import smtplib
from email.mime.text import MIMEText
import pytz
import time


if not mt5.initialize():
    print(" MT5 initialization failed")
    quit()

symbols = ["EURUSD", "GBPJPY", "CADJPY"]

#  Native timeframes only
native_timeframes = {
    "1H": mt5.TIMEFRAME_H1,
    "4H": mt5.TIMEFRAME_H4,
    "1D": mt5.TIMEFRAME_D1
}

kst = pytz.timezone('Asia/Seoul')

def get_pip_value(symbol):
    if "US30" in symbol or "HK50" in symbol:
        return 1.0
    elif "XAUUSD" in symbol:
        return 0.1
    elif "JPY" in symbol:
        return 0.01
    else:
        return 0.0001

def send_alert(msg):
    sender_email = "billikhlasdiyor@gmail.com"
    receiver_email = "billikhlasdiyor@gmail.com"
    app_password = "**********" #censored  
    subject = " Signal Alert: EMA + Pattern + S/R"
    email_msg = MIMEText(msg)
    email_msg["Subject"] = subject
    email_msg["From"] = sender_email
    email_msg["To"] = receiver_email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, email_msg.as_string())
        print(f"[{datetime.datetime.now()}] ✉️ Email sent")
    except Exception as e:
        print(f" Email error: {e}")

# Candle logic
def add_ema(df):
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    return df

def detect_doji_like(row):
    body = abs(row['close'] - row['open'])
    wick_top = row['high'] - max(row['close'], row['open'])
    wick_bottom = min(row['close'], row['open']) - row['low']
    total_range = row['high'] - row['low']
    body_ratio = body / total_range if total_range else 1
    wick_symmetry = abs(wick_top - wick_bottom) <= 0.2 * total_range
    return body_ratio < 0.1 and wick_symmetry

def is_bullish_engulfing(prev, curr):
    return prev['close'] < prev['open'] and curr['close'] > curr['open'] and curr['open'] < prev['close'] and curr['close'] > prev['open']

def is_bearish_engulfing(prev, curr):
    return prev['close'] > prev['open'] and curr['close'] < curr['open'] and curr['open'] > prev['close'] and curr['close'] < prev['open']

def is_pin_bar(row):
    body = abs(row['close'] - row['open'])
    wick_top = row['high'] - max(row['close'], row['open'])
    wick_bottom = min(row['close'], row['open']) - row['low']
    return (wick_top > 2 * body and wick_top > wick_bottom) or (wick_bottom > 2 * body and wick_bottom > wick_top)

def check_ema_cross(row):
    if row['EMA50'] > row['high']:
        return "EMA above"
    elif row['EMA50'] < row['low']:
        return "EMA below"
    elif row['low'] < row['EMA50'] < row['high']:
        return "EMA inside"
    return None

def is_ema_near(row, pip_value, min_pips=10, max_pips=20):
    center = (row['open'] + row['close']) / 2
    dist = abs(center - row['EMA50'])
    return min_pips * pip_value <= dist <= max_pips * pip_value

def detect_sr(df, sensitivity=3):
    support, resistance = [], []
    for i in range(sensitivity, len(df) - sensitivity):
        low = df['low'][i]
        high = df['high'][i]
        if all(low < df['low'][i - j] and low < df['low'][i + j] for j in range(1, sensitivity + 1)):
            support.append(low)
        if all(high > df['high'][i - j] and high > df['high'][i + j] for j in range(1, sensitivity + 1)):
            resistance.append(high)
    return support + resistance

def is_near_sr(row, levels, pip_value, buffer_pips=15):
    return any(abs(row['close'] - lvl) <= buffer_pips * pip_value for lvl in levels)

#Last alert tracker
last_alerts = {}

#  Main live loop
while True:
    now_kst = datetime.datetime.now(tz=kst).replace(minute=0, second=0, microsecond=0)

    for symbol in symbols:
        for label, tf in native_timeframes.items():
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, 100)
            if rates is None or len(rates) < 60:
                continue

            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul')
            df = add_ema(df)
            pip = get_pip_value(symbol)
            sr_levels = detect_sr(df)

            if len(df) >= 3:
                prev2, prev1, curr = df.iloc[-3], df.iloc[-2], df.iloc[-1]
                candle_open_kst = curr['time'].replace(minute=0, second=0, microsecond=0)
                alert_key = f"{symbol}_{label}"
                if now_kst == candle_open_kst:
                    if (
                        (detect_doji_like(prev1) or is_bullish_engulfing(prev2, prev1) or is_bearish_engulfing(prev2, prev1) or is_pin_bar(prev1))
                        and is_ema_near(prev1, pip)
                        and check_ema_cross(prev1)
                        and is_near_sr(prev1, sr_levels, pip)
                    ):
                        if last_alerts.get(alert_key) != prev1['time']:
                            last_alerts[alert_key] = prev1['time']
                            msg = (
                                f"[{symbol} - {label}] {prev1['time']}\n"
                                f" Signal: Pattern + EMA50 + S/R\n"
                                f"{check_ema_cross(prev1)}\n"
                                f"Price: {prev1['close']:.5f}, EMA50: {prev1['EMA50']:.5f}"
                            )
                            send_alert(msg)

    print(f"[{now_kst}]  Waiting 5 minutes...\n")
    time.sleep(300)

mt5.shutdown()
