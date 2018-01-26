# -*- coding: utf8 -*-

import tabulate
from bittrex.bittrex import Bittrex, API_V1_1
import json

bittrex_api_version = API_V1_1
table = [["Coin Name"], ["Last"], ["Coin Owned"], ["Net Worth"],["24h High"], ["24h Low"]]
table_content = [["BTC"], ["1"], ["2"], ["233"],["111"], ["545"]]

def auth_bittrex():
    dataBittrex = json.load(open('key.json'))
    bittrexApi = Bittrex(dataBittrex["api_secret"], dataBittrex["api_key"], api_version=bittrex_api_version)
    return bittrexApi

def main():
    bittrexApi = auth_bittrex()
    marketHistory = bittrexApi.get_marketsummary("BTC-XMR")
    print json.dumps(marketHistory, indent=2)
    print tabulate(table, tablefmt="plain")

if __name__ == '__main__':
    main()
