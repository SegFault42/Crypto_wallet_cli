# -*- coding: utf8 -*-

from tabulate import tabulate
from bittrex.bittrex import Bittrex, API_V1_1
import json
import types
import os
import time
import sys
from time import gmtime, strftime
from currency_converter import CurrencyConverter
import re

reload(sys)
sys.setdefaultencoding('utf8')
bittrex_api_version = API_V1_1

red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
white = "\033[97m"
end = "\033[0m"

percent = 0

header = [cyan + "Coin Name" + end,
            cyan + "BTC Price" + end,
            cyan + "USDT Price" + end,
            cyan + "Coin Owned" + end,
            cyan + "Buyed price" + end,
            cyan + "Total (BTC)" + end,
            cyan + "Total (USDT)" + end,
            cyan + "Total (EUR)" + end,
            cyan + "24h High" + end,
            cyan + "24h Low" + end]

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

def fillTable(bittrexApi, dataWallet):
    global totalBtcCmp
    table_content = []
    totalInBtc = 0
    totalInUSDT = 0
    c = CurrencyConverter()

    try:
        btcPrice = bittrexApi.get_market_summary("USDT-BTC")["result"][0]["Bid"]
    except:
        return None
    marketSummaries = getCoinsInfo(bittrexApi) # marketSummaries get all coins information
    if marketSummaries == None:
        return None
    for key, value in dataWallet.iteritems():
        if isinstance(value[0], types.FloatType) or isinstance(value[0], types.IntType):
            try:
                coinInfo = getCoinInfo(key, marketSummaries) # coinInfo get specific coin information 
            except:
                continue
            if coinInfo != None:
                totalCoinInBtc = (value[0] * coinInfo["Bid"])
                totalUSDT = btcPrice * totalCoinInBtc
                totalInBtc += totalCoinInBtc
                totalInUSDT += totalUSDT
                if value[1] == 0:
                    totalUSDT = ""
                    totalCoinInBtc = ""
                elif value[1] < coinInfo["Bid"]:
                    totalUSDT = totalUSDT
                    totalCoinInBtc = totalCoinInBtc
                else:
                    totalUSDT = totalUSDT
                    totalCoinInBtc = totalCoinInBtc
                totalEUR = c.convert(totalUSDT, 'USD', 'EUR')
                table_content.append([key, coinInfo["Bid"], coinInfo["Bid"] * btcPrice, value[0], value[1], totalCoinInBtc, totalUSDT, totalEUR, coinInfo["High"], coinInfo["Low"]])
    totalInEUR = c.convert(totalInUSDT, 'USD', 'EUR')
    table_content.append(["Total", None, None, None, None, totalInBtc, totalInUSDT, totalInEUR, None, None])
    return table_content

def coloriseTable(tableContent, oldTableContent):
    i = 0
    if (oldTableContent and tableContent):
        while i < len(tableContent):
            j = 1
            while j < len(tableContent[i]):
                regex = re.findall(r'[-+]?([0-9]*\.[0-9]+)', str(oldTableContent[i][j]))
                if (len(regex)):
                    if (tableContent[i][j]):
                        if (float(regex[0]) > float(tableContent[i][j])):
                            tableContent[i][j] = green + str(tableContent[i][j]) + end
                        elif (float(regex[0]) < float(tableContent[i][j])):
                            tableContent[i][j] = red + str(tableContent[i][j]) + end
                        else:
                            tableContent[i][j] = oldTableContent[i][j]
                    else:
                        tableContent[i][j] = oldTableContent[i][j]
                else:
                    tableContent[i][j] = oldTableContent[i][j]
                j = j + 1
            i = i + 1
    print tabulate(tableContent, header, floatfmt=".8f", tablefmt="fancy_grid")

def main():
    dataWallet = json.load(open('wallet.json')) # get all info in wallet.json
    bittrexApi = auth_bittrex()
    oldTableContent = None
    tableContent = None

    while True:
        tableContent = fillTable(bittrexApi, dataWallet)
        print("\033[H\033[J") # print at top left
        if (tableContent == None):
            print "\033[31mFailed to retrieve data ! Retrying ...\033[0m"
        else:
            if (oldTableContent == None):
                print tabulate(tableContent, header, floatfmt=".8f", tablefmt="fancy_grid")
            else:
                coloriseTable(tableContent, oldTableContent)
            oldTableContent = tableContent[:]
        print "Last refresh : " + strftime("%Y-%m-%d %H:%M:%S", gmtime())

if __name__ == '__main__':
    main()
