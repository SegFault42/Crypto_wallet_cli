# -*- coding: utf8 -*-

from tabulate import tabulate
from bittrex.bittrex import Bittrex, API_V1_1
import json
import types
import os
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')


bittrex_api_version = API_V1_1
header = ["Coin Name", "Last", "Coin Owned", "Buyed price", "Net Worth (BTC)", "Net Worth (USDT)", "24h High", "24h Low"]

def auth_bittrex():
    dataBittrex = json.load(open('key.json'))
    bittrexApi = Bittrex(dataBittrex["api_secret"], dataBittrex["api_key"], api_version=bittrex_api_version)
    return bittrexApi

def getCoinInfo(bittrexApi, coin):
    marketHistory = bittrexApi.get_marketsummary("BTC-" + coin)
    return marketHistory

def parseWallet_json(bittrexApi):
    table_content = []
    dataWallet = json.load(open('wallet.json'))
    for key, value in dataWallet.iteritems():
        if isinstance(value[0], types.FloatType):
            coinInfo = getCoinInfo(bittrexApi, key)
            btcPrice = bittrexApi.get_marketsummary("USDT-BTC")["result"][0]["Last"]
            netWorth = (coinInfo["result"][0]["Last"] - value[1]) * value[0]
            netWorthUSDT = btcPrice * netWorth
            if netWorth > 0:
                netWorth = "\033[32m   " + str(netWorth) + "\033[0m"
            else:
                netWorth = "\033[31m   " + str(netWorth) + "\033[0m"
            table_content.append([key, coinInfo["result"][0]["Last"], value[0], value[1], netWorth, netWorthUSDT, coinInfo["result"][0]["High"], coinInfo["result"][0]["Low"]])
    return table_content

def main():
    bittrexApi = auth_bittrex()
    while True:
        table_content = parseWallet_json(bittrexApi)
        print("\033[H\033[J") # print a top left
        print tabulate(table_content, header, floatfmt=".12f", tablefmt="fancy_grid")

if __name__ == '__main__':
    main()
