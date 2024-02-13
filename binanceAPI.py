from os import environ
from datetime import datetime, timezone, timedelta
from cybotrade.strategy import Strategy as BaseStrategy
from cybotrade.models import (
    OrderParams,
    OrderSide,
    RuntimeMode,
    RuntimeConfig,
    Exchange,
)
import numpy as np
import asyncio
import logging
import colorlog
import random
import requests
from binance import Client
import json
import collections
import time
import pandas as pd
import matplotlib.pyplot as plt


def fetch_kline_price_data():
    # API_Library = "v1/premiumIndexKlines"  # https://binance-docs.github.io/apidocs/futures/en/#mark-price-kline-candlestick-data, API 連結
    API_Library = "v1/klines"
    ticker = "BTCUSDT"  # 交易對
    time_interval = (
        "1d"  # 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    )
    start_time = datetime(
        2020,
        1,
        1,
    )  # 取得資料開始的時間，YYYY/M/D，回測至少三年，不用太久
    end_time = datetime.now()  # 資料最新更新的時間，也可以自己設定時間

    price_data = []

    while start_time < end_time:
        start_time_2 = int(start_time.timestamp() * 1000)
        url = (
            "https://fapi.binance.com/fapi/"
            + str(API_Library)
            + "?symbol="
            + str(ticker)
            + "&interval="
            + str(time_interval)
            + "&limit=1500&startTime="
            + str(start_time_2)
        )
        # print(start_time)
        resp = requests.get(url)
        resp = json.loads(resp.content.decode())

        price_data.extend(resp)

        start_time = start_time + timedelta(minutes=1500)

    price_data = pd.DataFrame(price_data)

    price_data[0] = pd.to_datetime(price_data[0], unit="ms")
    price_data[6] = pd.to_datetime(price_data[6], unit="ms")

    # 項目命名Columns Rename
    price_data.columns = [
        "Time",
        "Open",
        "High",
        "Low",
        "Close",
        # "Ignore",
        "Volume",
        "Close Time",
        "Ignore",
        "Ignore",
        "Ignore",
        "Ignore",
        "Ignore",
    ]
    price_data = price_data.set_index("Time")

    # price_data = price_data[price_data.index >= datetime(2020, 12, 1)]

    extracted_df = price_data["Close"]

    return extracted_df

    # return price_data


price_request = fetch_kline_price_data()

price_df = pd.DataFrame(price_request)
print(price_df)

new_df = price_df.to_csv("price_data.csv")
