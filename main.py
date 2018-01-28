# -*- coding: utf8 -*-

from tabulate import tabulate
import progressbar
from bittrex.bittrex import Bittrex, API_V1_1
import json
import types
import os
import time
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

bittrex_api_version = API_V1_1
header = ["Coin Name", "Bid", "Coin Owned", "Buyed price", "Total (BTC)", "Total (USDT)", "24h High", "24h Low"]

def auth_bittrex():
    dataBittrex = json.load(open('key.json'))
    bittrexApi = Bittrex(dataBittrex["api_secret"], dataBittrex["api_key"], api_version=bittrex_api_version)
    return bittrexApi

def getCoinsInfo(bittrexApi):
    marketSummaries = bittrexApi.get_market_summaries()
    return marketSummaries

def getCoinInfo(coin, marketSummaries):
    #print "marketSummaries = " + marketSummaries["result"][0]["MarketName"]
    for market in marketSummaries["result"]:
        if (market["MarketName"] == "BTC-" + coin):
            return market
    return None


def parseWallet_json(bittrexApi):
    table_content = []
    dataWallet = json.load(open('wallet.json'))
    coinsInfo = getCoinsInfo(bittrexApi)
    #print json.dumps(coinsInfo, indent = 2)
    for key, value in dataWallet.iteritems():
        if isinstance(value[0], types.FloatType):
            coinInfo = getCoinInfo(key, coinsInfo)
            if coinInfo != None:
                totalBtc = coinInfo["Bid"] * value[0]
                btcPrice = bittrexApi.get_marketsummary("USDT-BTC")["result"][0]["Bid"]
                netWorthUSDT = btcPrice * totalBtc
                if totalBtc > 0:
                    totalBtc = "\033[32m ⬆  " + str(totalBtc) + "\033[0m"
                else:
                    totalBtc = "\033[31m ⬇  " + str(totalBtc) + "\033[0m"
                table_content.append(["\033[35m" + key + "\033[0m", coinInfo["Bid"], value[0], value[1], totalBtc, netWorthUSDT, coinInfo["High"], coinInfo["Low"]])
                #print "Info for " + key + " Receveid"
    return table_content

def main():
    bittrexApi = auth_bittrex()
    #i = 0
    while True:
        table_content = parseWallet_json(bittrexApi)
        print("\033[H\033[J") # print at top left
        print tabulate(table_content, header, floatfmt=".8f", tablefmt="fancy_grid")
        print "Last refresh : " + str(datetime.datetime.now())
        #print i
        #i += 1

if __name__ == '__main__':
    main()
