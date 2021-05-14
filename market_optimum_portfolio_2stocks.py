import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Steps:
# - Define the risk free (rf) asset (10 year US bond yield) --> ^TNX
# - Follow the same structure as mvp

def stock_download(ticker):
    stock = yf.download(tickers=ticker, period='1y', interval='1d')
    return stock

rf = stock_download('^TNX')
print(rf) # variance = 0