#import modules
from ctypes import sizeof
from email.quoprimime import quote
from operator import concat
from os import set_inheritable
from py_compile import _get_default_invalidation_mode
import pandas as pd
import yfinance as yf
import yahoofinancials as yahoof
import matplotlib.pyplot as plt
import fundamentalanalysis as fa
from csv import reader
import json
from time import sleep, time
from datetime import datetime
from colorama import Fore, Back, Style

#matplotlib inline
## pwd: uhEPCxN7wztRExHjhjJvPX42g7Ps2bu3aHt6oVMjoaY
#retrieve the basic data for a stock

# fd_key = "8936003df49ba9f1291606bbc108d23a"

tick_fields = ['Ticker','Total Shares','Invest Value']
data_key = ['Symbol', 'Total Shares', 'Invest Value']
reader_keys = ["symbol",  "price", "dayHigh", "dayLow", "open", "change"]
extract_data_keys = ['regularMarketPrice', 'regularMarketDayHigh', 'regularMarketChange']

#Global data list
tech_stocks = []
index_funds = []
consumer_stocks = []

global_stock_dict = {'Technology' : tech_stocks, 'Index' : index_funds, 'Consumer' : consumer_stocks}
global_stock_op = []

# for tick in ticker:
#     st_data = yf.Ticker("MSFT")

# for tick in ticker:
#     st_data = yahoof.YahooFinancials(tick)
#     print(st_data.get_current_price())


#
# stock_data = yf.download('AAPL', start='2022-04-01', end='2022-04-13', progress=False)

#print the data found
# print(stock_data.tail())
# print(st_data.get_dividends())

# # Plot adjusted close price data
# stock_data['Adj Close'].plot()
# plt.show()

#quotes = fa.quote("MSFT", fd_key)

#print(quotes)
#quotes.to_csv('MSFT.csv')

# def getStockPrice():
#     tot_val = 0
#     with open("stocks.json", "r") as infile:
#         j_read = json.load(infile)
#         for ele in j_read['Stocks']:
#             tick = ele.get('Ticker')
#             stock_quote = yahoof.YahooFinancials(tick)
#             t_price = stock_quote.get_current_price()
#             tot_shares = ele.get('Total Shares')
#             tick_val = ele['Total_Equity'] = t_price * tot_shares
#             tot_val += tick_val
#             sleep(2)

#     with open("Stocks.json", "w") as outfile:
#         json.dump(j_read, outfile, indent=4)
    
#     displayTotalEquity(tot_val)

# def readCsv(infile, outfile):
#     quotes = {}
#     jstock_list = []

#     rd_obj = pd.read_csv('stock_list.csv', skipinitialspace=True, usecols=tick_fields)
#     for index, row in rd_obj.iterrows():
#         quotes.update(row.to_dict())
#         print(quotes)
#         print("\n")
#         jstock_list.append(quotes.copy())

#     json_table = {'Stocks' : jstock_list}
#     print(json_table)
#     with open("stocks.json", "w") as outfile:
#         json.dump(json_table, outfile, indent=4)
#         outfile.write(json_table)

def updatePrices():
    tot_val = 0
    with open("stocks.json", "r") as infile:
        j_read = json.load(infile)
        for st_op in global_stock_op:
            tick = st_op['Symbol']
            for ele in j_read['Stocks']:
                if ele.get('Ticker') == tick:
                    tick_price = st_op['regularMarketPrice']
                    tot_shares = ele.get('Total Shares')
                    tick_val = ele['Total_Equity'] = tick_price * tot_shares
                    tot_val += tick_val
    
    with open("Stocks.json", "w") as outfile:
        json.dump(j_read, outfile, indent=4)
    
    displayTotalEquity(tot_val)

def extractStockInfo(tick, tick_data):
    ini_data = {'Symbol': tick}
    for t in extract_data_keys:
        ini_data.update({t: tick_data.get(t)})
    global_stock_op.append(ini_data)

def displayTotalEquity(latest_val):
    print("\n.......Total Value of Investments......\n")
    print("\t\t", latest_val)

def constructData():
    with open("stocks.json", "r") as infile:
        j_read = json.load(infile)
        for ele in j_read['Stocks']:
            sector = ele.get('Sector')
            global_stock_dict[sector].append(ele.get('Ticker'))
        
        for sector in global_stock_dict:
            global_stock_dict[sector] = list(set(global_stock_dict[sector]))

def get_sector_data(ticker_list):
    #start_time = datetime.now()
    stock_data = yahoof.YahooFinancials(ticker_list)
    #print("Time taken to access API: ", (datetime.now() - start_time))
    #print("\n")
    return stock_data

def get_stock_list_data():
    for sector in global_stock_dict:
        stock_data = get_sector_data(global_stock_dict[sector])
        st_data = stock_data.get_stock_price_data()
        for key in st_data:
            extractStockInfo(key, st_data[key])

def getInvestValue():
    inv_val = 0
    with open("stocks.json", "r") as infile:
        j_read = json.load(infile)
        for ele in j_read['Stocks']:
            inv_val += ele.get('Total Value')
    
    return inv_val

def main():
    print(".....Starting Stock Tracker.....\n")
    #getStockPrice()
    constructData()
    get_stock_list_data()
    updatePrices()

    total_invest_val = getInvestValue()
    print("\n.......Total Value of Investments......\n")
    print("\t\t", Back.GREEN + str(total_invest_val))
    print(Style.RESET_ALL)
    print("\n\n")
    print(".....Stock Tracker Completed.....\n")

if __name__ == '__main__':
    main()