import quandl
import pickle
import os.path
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from constants import *
import datetime

class StockGatherer():
    def __init__(self):
        quantl_key_file = open("apikey", "r")
        self.quantl_key = quantl_key_file.read()[0:-1]
        quandl.ApiConfig.api_key = self.quantl_key
        self.remake = False
        if self.remake:
            self.repullData()

    #Get the data for a single stock
    def getData(self, stock):
        """
        returns a tuple of two lists, (dates, endPrices)
        Also curretly prints a graph in Python
        """
        fileData = pickle.load( open(stock + ".p", "rb"))
        endPrices = []
        dates = []

        for x in fileData:
            dates.append(x[0])
            endPrices.append(x[1])
        plt.plot(dates, endPrices)
        plt.show()
        return (stock, dates, endPrices)

    #TODO: GET VARIABLE TIMES
    def repullData(self, time = 6):
        """
        Repulls all data from quandl
        HARDCODED TO LAST 6 MONTHS RN (time)
        """
        for x in LOOKUP_TABLE:
            print(x)
            now = datetime.datetime.now()
            six_months_ago = int(now.strftime("%m"))-time
            now.strftime("%Y-%m-%d")
            lookup = now.strftime("%Y-") + str(six_months_ago) + now.strftime("-%d")
            tempData = quandl.get("EOD/"+LOOKUP_TABLE[x], start_date=lookup, column_index = '4', returns="numpy")
            pickle.dump(tempData, open(FILE_NAMES[x], "wb"))

    def pullSingleData(self, stock):
        """
        takes in the Stock (acronym? 1-4 letter thing)
        Pulls the stock data again from quandl
        returns nothing
        HARDCODED TO LAST 6 MONTHS RN
        """
        now = datetime.datetime.now()
        six_months_ago = int(now.strftime("%m"))-6
        now.strftime("%Y-%m-%d")
        lookup = now.strftime("%Y-") + str(six_months_ago) + now.strftime("-%d")
        tempData = quandl.get("EOD/"+stock, start_date=lookup, column_index = '4', returns="numpy")
        pickle.dump(tempData, open(stock + ".p", "wb"))

if __name__ == "__main__":
    gatherer = StockGatherer()
    print(gatherer.getData('V'))
