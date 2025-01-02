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


def main():

    print(get_asset_balance(BASE_ASSET))
    print(get_asset_balance(QUOTE_ASSET))

    print()

    print(get_minimum_quantity(SYMBOL))

    print()

    print(get_quantity_step(SYMBOL))

    print()

    print(get_minimum_notional(SYMBOL))

if __name__ == "__main__":
    main()
