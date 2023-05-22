import pandas as pd
#Yahoo Finance API
import yfinance as yf

def download_historical_data(ticker):
    # Download historical data as pandas DataFrame
    data = yf.download(ticker, start="1900-01-01", end="2023-05-22")    
    return data

data = download_historical_data("^GSPC") #S&P500 ticker 
print(data)
df.to_csv('historical_SPdata.csv', index = False)