# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:01:02 2022

@author: Korey
"""

from alpha import core_api as a

# pass in your own api_key
api_key = '296ULICGSB63VL7A' 

# ------------- EQUITY CONSTRUCTOR -----------

# tickers is a list of symbols represented an equity which is traded on major indices


tickers = ['T','NVDA', 'SHOP', 'INTC', 'VZ', 'AMZN', 'GOOG', 'AAPL',
           'F', 'MSFT', 'CRM', 'IGLB', 'VOO', 'SPY', 'XLK', 'VB']


# reduce calls to speed up samples
tickers = tickers[0:2]


# add a start and end date for all equity graphs if desired
start_end_dates = ('2018-01-01', '2022-10-07')


# call the class constructer, pass in api_key and tickers 
equities = a.Equities(api_key=api_key, tickers=tickers)



# ---- E#QUITY DATAFRAMES ----

# cashflows
cf = equities.get_cashflow()

# get time series daily adjusted
tsa_df = equities.get_time_series_daily_adjusted()


# ---- EQUITY SUBPLOTS ----

# call the subplot method and call fig.show
fig = equities.daily_adjusted_subplot(start_end_dates=start_end_dates, output_size='full')
fig.show()


fig = equities.cashflow_subplot()
fig.show()