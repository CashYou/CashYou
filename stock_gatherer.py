import quandl
import pickle
import os.path
from pathlib import Path
import numpy as np
#import matplotlib.pyplot as plt
from Constants import *
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter


class StockGatherer():
    def __init__(self):
        # quantl_key_file = open("apikey", "r")
        # self.quantl_key = quantl_key_file.read()[0:-1]
        # quandl.ApiConfig.api_key = self.quantl_key
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
        #plt.plot(dates, endPrices)
        #plt.show()
        return (stock, dates, endPrices)

    def getGraph(self, stock):
        """
        sets up and returns the bokeh graph visualization object
        """
        stock, dates, endPrices = self.getData(stock)
        self.graph1 = figure(title=stock, plot_width=900, plot_height=400)
        self.graph1.line(x=dates, y=endPrices, line_width = 2, line_color = 'blue')
        self.graph1.xaxis.formatter=DatetimeTickFormatter(
                hours = ['%d %B %Y'],
                days = ['%d %B %Y'],
                months = ['%d %B %Y'],
                years = ['%d %B %Y'],
            )
        return self.graph1


    # TODO: GET VARIABLE TIMES
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
    # print(gatherer.getData('V'))
