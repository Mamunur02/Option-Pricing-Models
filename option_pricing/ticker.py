# Importing libraries
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

# Class for fetching data from yahoo finance
class Ticker:

    # Fetches stock data
    @staticmethod
    def get_historical_data(ticker):
        data = yf.Ticker(ticker).history(period='1y', auto_adjust=False)
        return data

    # Gets dataframe columns from previously fetched stock data
    @staticmethod
    def get_columns(data):
        return [column for column in data.columns]

    # Returns last available price for specified column from fetched data
    @staticmethod
    def get_last_price(data, column_name):
        return data[column_name].iloc[len(data)-1]

    # Calculates historical annualized volatility of the stock
    @staticmethod
    def get_volatility(data, column_name):
        data['Daily Return'] = data[column_name].pct_change().dropna()
        daily_volatility = data['Daily Return'].std()
        annual_volatility = daily_volatility * np.sqrt(252)
        return annual_volatility

    # Plots specified column values from data
    @staticmethod
    def plot_data(data, ticker, column_name):
        fig, ax = plt.subplots()
        data[column_name].plot(ax=ax)
        ax.set_ylabel(f'{column_name}')
        ax.set_xlabel('Date')
        ax.set_title(f'Historical data for {ticker} - {column_name}')
        ax.legend(loc='best')
        return fig