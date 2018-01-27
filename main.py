# -*- coding: utf8 -*-

from tabulate import tabulate
from bittrex.bittrex import Bittrex, API_V1_1
import json
import types
import os
import time

bittrex_api_version = API_V1_1
header = ["Coin Name", "Last", "Coin Owned", "Buyed price", "Net Worth", "24h High", "24h Low"]
#table_content = [["", 0.0, 0.0, 0.0, 0.0, 0.0]]

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
    #print json.dumps(dataWallet, indent=2)
    for key, value in dataWallet.iteritems():
        if isinstance(value[0], types.FloatType):
            coinInfo = getCoinInfo(bittrexApi, key)
            netWorth = coinInfo["result"][0]["Last"] - value[1]
            table_content.append([key, coinInfo["result"][0]["Last"], value[0], value[1], netWorth * value[0], coinInfo["result"][0]["High"], coinInfo["result"][0]["Low"]])
            #table_content[0][0] = key
            #table_content[0][2] = value[0]
            #table_content[0][3] = value[1]
            ##print "%.8f" % (dataWallet[i][0])
            ##print "%.8f" % (dataWallet[i][1])
            #print dataWallet
    return table_content

def main():
    bittrexApi = auth_bittrex()
    while True:
        table_content = parseWallet_json(bittrexApi)
        print("\033[H\033[J")
        print tabulate(table_content, header, floatfmt=".8f", tablefmt="fancy_grid")
        #time.sleep(2)

if __name__ == '__main__':
    main()
