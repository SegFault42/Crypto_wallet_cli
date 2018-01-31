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

cyan = "\033[36m"
end = "\033[0m"

header = [cyan + "Coin Name" + end,
            cyan + "BTC Price" + end,
            cyan + "USDT Price" + end,
            cyan + "Coin Owned" + end,
            cyan + "Buyed price" + end,
            cyan + "Total (BTC)" + end,
            cyan + "Total (USDT)" + end
            , cyan + "24h High" + end ,
            cyan + "24h Low" + end]

totalBtcCmp = 0

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
    global totalBtcCmp
    table_content = []
    dataWallet = json.load(open('wallet.json'))
    coinsInfo = getCoinsInfo(bittrexApi)
    if coinsInfo == None:
        return None, None, None
    totalInBtc = 0
    totalInUSDT = 0
    for key, value in dataWallet.iteritems():
        if isinstance(value[0], types.FloatType) or isinstance(value[0], types.IntType):
            if coinsInfo != None:
                try:
                    coinInfo = getCoinInfo(key, coinsInfo)
                except:
                    continue
            if coinInfo != None:
                try:
                    btcPrice = bittrexApi.get_marketsummary("USDT-BTC")["result"][0]["Bid"]
                except:
                    continue
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
    if totalBtcCmp > totalInBtc:
        table_content.append(["Total", None, None, None, None, "\033[31m ⬇ " + str(totalInBtc) + "\033[0m", "\033[31m ⬇ " + str(totalInUSDT) + "\033[0m", None, None])
    elif totalBtcCmp <= totalInBtc:
        table_content.append(["Total", None, None, None, None, "\033[32m ⬆ " + str(totalInBtc) + "\033[0m", "\033[32m ⬆ " + str(totalInUSDT) + "\033[0m", None, None])
    totalBtcCmp = totalInBtc
    return table_content, totalInBtc, totalInUSDT

def main():
    bittrexApi = auth_bittrex()
    while True:
        table_content, totalBtc, totalUsdt = fillTable(bittrexApi)
        print("\033[H\033[J") # print at top left
        if (table_content == None):
            print "\033[31mFailed to retrieve data ! Retrying ...\033[0m"
        else:
            print tabulate(table_content, header, floatfmt=".8f", tablefmt="fancy_grid")
        print "Last refresh : " + strftime("%Y-%m-%d %H:%M:%S", gmtime())

if __name__ == '__main__':
    main()
