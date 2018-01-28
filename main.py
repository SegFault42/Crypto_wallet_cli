# -*- coding: utf8 -*-

from tabulate import tabulate
import progressbar
from bittrex.bittrex import Bittrex, API_V1_1
import json
import types
import os
import time
import sys
from time import gmtime, strftime

reload(sys)
sys.setdefaultencoding('utf8')
bittrex_api_version = API_V1_1
header = ["Coin Name", "BTC Price", "USDT Price", "Coin Owned", "Buyed price", "Total (BTC)", "Total (USDT)", "24h High", "24h Low"]

def auth_bittrex():
    dataBittrex = json.load(open('key.json'))
    bittrexApi = Bittrex(dataBittrex["api_secret"], dataBittrex["api_key"], api_version=bittrex_api_version)
    return bittrexApi

def getCoinsInfo(bittrexApi):
    marketSummaries = bittrexApi.get_market_summaries()
    return marketSummaries

def getCoinInfo(coin, marketSummaries):
    for market in marketSummaries["result"]:
        if (market["MarketName"] == "BTC-" + coin):
            return market
    return None

def fillTable(bittrexApi):
    table_content = []
    dataWallet = json.load(open('wallet.json'))
    coinsInfo = getCoinsInfo(bittrexApi)
    #print json.dumps(coinsInfo, indent=2)
    totalInBtc = 0
    totalInUSDT = 0
    for key, value in dataWallet.iteritems():
        if isinstance(value[0], types.FloatType) or isinstance(value[0], types.IntType):
            coinInfo = getCoinInfo(key, coinsInfo)
            if coinInfo != None:
                btcPrice = bittrexApi.get_marketsummary("USDT-BTC")["result"][0]["Bid"]
                totalCoinInBtc = (value[0] * coinInfo["Bid"])
                totalUSDT = btcPrice * totalCoinInBtc
                totalInBtc += totalCoinInBtc
                totalInUSDT += totalUSDT
                if value[1] < coinInfo["Bid"]:
                    totalUSDT = "\033[32m ⬆ " + str(totalUSDT) + "\033[0m"
                    totalCoinInBtc = "\033[32m ⬆ " + str(totalCoinInBtc) + "\033[0m"
                else:
                    totalUSDT = "\033[31m ⬇ " + str(totalUSDT) + "\033[0m"
                    totalCoinInBtc = "\033[31m ⬇ " + str(totalCoinInBtc) + "\033[0m"
                table_content.append([key, coinInfo["Bid"], coinInfo["Bid"] * btcPrice, value[0], value[1], totalCoinInBtc, totalUSDT, coinInfo["High"], coinInfo["Low"]])
    return table_content, totalInBtc, totalInUSDT

def main():
    bittrexApi = auth_bittrex()
    while True:
        table_content, totalBtc, totalUsdt = fillTable(bittrexApi)
        print("\033[H\033[J") # print at top left
        print tabulate(table_content, header, floatfmt=".8f", tablefmt="fancy_grid")
        print "\033[34mTotal in BTC = \033[33m" + str(totalBtc)
        print "\033[34mTotal in USDT = \033[33m" + str(totalUsdt) + "\033[0m"
        print "Last refresh : " + strftime("%Y-%m-%d %H:%M:%S", gmtime())

if __name__ == '__main__':
    main()
