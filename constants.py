import random #Just in case

#a table of the companies we can look up
LOOKUP_TABLE = {"Visa Inc.":"V", "UnitedHealth Group Incorporated":"UNH", "Procter & Gamble Company [The]":"PG", "Coca-Cola Company [The]":"KO", "Goldman Sachs Group Inc. [The]":"GS", "Wal-Mart Stores Inc.":"WMT", "Merck & Company Inc.":"MRK", "Verizon Communications Inc.":"VZ", "United Technologies Corporation":"UTX", "The Travelers Companies Inc.":"TRV",
                "Walt Disney Company (The)":"DIS", "Boeing Company (The)":"BA", "General Electric Company":"GE", "Home Depot Inc. (The)":"HD", "3M Company":"MMM", "Pfizer Inc":"PFE", "Nike Inc.":"NKE", "McDonald's Corporation":"MCD", "JP Morgan Chase & Co.":"JPM", "Intel Corporation":"INTC",
                "Cisco Systems Inc.":"CSCO", "Chevron Corporation":"CVX", "Caterpillar, Inc.":"CAT", "American Express Company":"AXP", "Johnson & Johnson":"JNJ", "Exxon Mobil Corporation":"XOM", "Microsoft Corporation":"MSFT", "International Business Machines Corporation":"IBM", "Apple Inc.":"AAPL"}

FILE_NAMES = {}
for x in LOOKUP_TABLE:
    FILE_NAMES[x] = LOOKUP_TABLE[x] + ".p"

# FILE_LAST_UPDATE = []
#TODO: IMPLEMENT REGULAR UPDATES
