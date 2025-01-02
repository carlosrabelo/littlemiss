from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
import os
import time
import pandas as pd
import math

load_dotenv(dotenv_path=".env/config")

API_KEY = os.getenv("BINANCE_KEY")
SECRET_KEY = os.getenv("BINANCE_SEC")
BASE_ASSET = os.getenv("BASE_ASSET")
QUOTE_ASSET = os.getenv("QUOTE_ASSET")
TIMEZONE = os.getenv("TIMEZONE")

client = Client(API_KEY, SECRET_KEY)

SYMBOL = BASE_ASSET + QUOTE_ASSET

INTERVAL = client.KLINE_INTERVAL_1HOUR 

def get_asset_balance(asset):
    asset_balance = 0.0  # Valor padrão para o saldo do ativo
    try:
        account_info = client.get_account()
        # Usando o fallback 0.0 e convertendo para float na mesma linha
        asset_balance = float(next((balance["free"] for balance in account_info["balances"] if balance["asset"] == asset), 0.0))
    except Exception as e:
        print(f"Erro ao obter saldo para {asset}: {e}")
    return asset_balance

def get_minimum_quantity(symbol):
    minimum_quantity = 0.0  # Valor padrão para a quantidade mínima
    try:
        symbol_info = client.get_symbol_info(symbol)
        # Usando o fallback 0.0 e convertendo para float na mesma linha
        minimum_quantity = float(next((f["minQty"] for f in symbol_info["filters"] if f["filterType"] == "LOT_SIZE"), 0.0))
    except Exception as e:
        print(f"Erro ao obter a quantidade mínima para {symbol}: {e}")
    return minimum_quantity

def get_quantity_step(symbol):
    quantity_step = 0.0  # Valor padrão para o step da quantidade
    try:
        symbol_info = client.get_symbol_info(symbol)
        # Usando o fallback 0.0 e convertendo para float na mesma linha
        quantity_step = float(next((f["stepSize"] for f in symbol_info["filters"] if f["filterType"] == "LOT_SIZE"), 0.0))
    except Exception as e:
        print(f"Erro ao obter stepSize para {symbol}: {e}")
    return quantity_step

def get_minimum_notional(symbol):
    minimum_notional = 0.0  # Valor padrão para o valor mínimo notional
    try:
        symbol_info = client.get_symbol_info(symbol)
        # Usando o fallback 0.0 e convertendo para float na mesma linha
        minimum_notional = float(next((f["minNotional"] for f in symbol_info["filters"] if f["filterType"] == "NOTIONAL"), 0.0))
    except Exception as e:
        print(f"Erro ao obter o valor mínimo notional para {symbol}: {e}")
    return minimum_notional

def get_candles_data(symbol, interval):
    try:
        candles = client.get_klines(symbol=symbol, interval=interval, limit=1000)
        if not candles:
            raise ValueError("Não foram encontradas velas para este simbolo e intervalo.")
        data = pd.DataFrame(
            candles,
            columns=[
                "open_time", "open", "high", "low", "close", "volume", 
                "close_time", "quote_asset_volume", "number_of_trades", 
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume",
                "ignore",
            ],
        )
        data = data[["close", "close_time"]]
        data["close"] = data["close"].astype(float)
        data["close_time"] = (pd.to_datetime(data["close_time"], unit="ms").dt.tz_localize("UTC").dt.tz_convert(TIMEZONE))
        return data
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return pd.DataFrame()

def calculate_moving_averages(data, fast_window=7, slow_window=25):
    try:
        fast_ma = data["close"].rolling(window=fast_window).mean()
        slow_ma = data["close"].rolling(window=slow_window).mean()

        last_fast_ma = fast_ma.iloc[-1]
        last_slow_ma = slow_ma.iloc[-1]

        return last_fast_ma, last_slow_ma
    except Exception as e:
        print(f"Erro ao calcular as medias moveis: {e}")
        return data

def main():

    candles_data = get_candles_data(SYMBOL, INTERVAL)

    last_fast_ma, last_slow_ma = calculate_moving_averages(candles_data)

    print(f"last_fast_ma: {last_fast_ma}")
    print(f"last_slow_ma: {last_slow_ma}")

if __name__ == "__main__":
    main()
