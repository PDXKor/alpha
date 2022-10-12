# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:13:35 2022

@author: Korey
"""

import alpha as a
import plotly as plt

# pass in your own api_key
api_key = '296ULICGSB63VL7A' 




# ------------- EQUITY CONSTRUCTOR -----------

# tickers is a list of symbols represented an equity which is traded on major indices
tickers = ['T','NVDA', 'SHOP', 'INTC', 'VZ', 'AMZN', 'GOOG', 'AAPL',
           'F', 'MSFT', 'CRM', 'IGLB', 'VOO', 'SPY', 'XLK', 'VB']

# add a start and end date for all equity graphs if desired
start_end_dates = ('2018-01-01', '2022-10-07')

# call the class constructer, pass in api_key and tickers 
equities = a.Equities(api_key=api_key, tickers=tickers)



# ---- EQUITY DATAFRAMES ----

# cashflows
cf = equities.get_cashflow()
print(cf.columns)

fig = equities.cashflow_subplot()
fig.show()

'''
colors = plt.colors.DEFAULT_PLOTLY_COLORS

# plot operating cash flow
columns = ['operatingCashflow','netIncome']
subplot_data = []
for t in tickers:
    df = cf[cf['ticker']==t]
    if not df.empty:
       
        subplot = {'subplot': [],
                   'title': t}
        
        for i,v in enumerate(columns):
            series = df[v]
            series = series.rename('value')
            subplot['subplot'].append({'series':series,
                                       'legend-name':v,
                                       'line-color':colors[i],
                                       },
                                      )
        subplot_data.append(subplot)
        
#print(subplot_data)
fig = a.alpha_subplots(subplot_data)
fig.show() 

'''
        
'''
# plot net income
cf = equities.get_cashflow()

subplot_data = []
for t in tickers:
    df = cf[cf['ticker']==t]
    if not df.empty:
        series = df[['operatingCashflow','netIncome']]
        series = series.rename({'netIncome':'value'},axis='columns')
        subplot = {'subplot': [{'series': series,
                                'legend-name': t}],
                   'title': t}
        subplot_data.append(subplot)
        
fig = a.alpha_subplots(subplot_data,title='Net Income')
fig.show() 
'''  




# get time series daily adjusted
#tsa_df = equities.get_time_series_daily_adjusted()



# ---- EQUITY SUBPLOTS ----

# call the subplot method and call fig.show
fig = equities.daily_adjusted_subplot(start_end_dates=start_end_dates, output_size='full')
fig.show()







# ----- ECONOMIC DATAFRAMES

econ = a.Economics(api_key)

# ten year treasury yield
ty_ten = econ.treasury_yield()
ty_ten = ty_ten[(ty_ten.index > '2002-01-01')]

# seven year treasury yield
ty_seven = econ.treasury_yield(maturity='7year')
ty_seven = ty_seven[(ty_seven.index > '2002-01-01')]

# two year treasury yield
ty_two = econ.treasury_yield(maturity='2year')
ty_two = ty_two[(ty_two.index > '2002-01-01')]

# get real gdp data - do date filtering outside of function call
rgdp = econ.real_gdp()
rgdp = rgdp[(rgdp.index > '2018-01-01')]

# get non farm payroll data
nfpr = econ.nonfarm_payroll()
nfpr = nfpr[(nfpr.index > '2018-01-01')]
#rgdp = rgdp[(rgdp['date'] > '2019-01-01') & (rgdp['date'] <= '2022-10-05')]

# get federal funds rate
ffr = econ.federal_funds_rate()
#ffr = ffr[(ffr.index > '2018-01-01')]

# get cpi
cpi = econ.cpi()
cpi = cpi[(cpi.index > '2018-01-01')]

# get consumer sentiment
cs = econ.consumer_sentiment()
cs = cs[(cs.index > '2018-01-01')]

# get inflation
infl = econ.inflation()
infl = infl[(infl.index > '2018-01-01')]


# -----MANUALLY CALL SUBPLOT

# call subplot function
fig = a.alpha_subplots(data=[{'subplot': [{'series': ty_ten,
                                      'legend-name': 'Ten Year Yield'},
                                     {'series': ty_seven,
                                      'legend-name': 'Seven Year Yield'},
                                     {'series': ty_two,
                                      'legend-name': 'Two Year Yield'}],
                            'title': 'Treasury Yields'},
                           {'subplot': [
                               {'series': rgdp,
                                'legend-name': 'Real GDP'}],
                           'title': 'Real GDP'},
                           {'subplot': [
                               {'series': nfpr,
                                'legend-name': 'Non Farm Payroll'}],
                           'title': 'Non Farm Payroll'},
                           {'subplot': [
                               {'series': ffr, 'legend-name': 'Federal Funds Rate'}], 'title': 'Federal Funds Rate'},
                           {'subplot': [{'series': cpi, 'legend-name': 'CPI'}],
                               'title': 'Consumer Price Index'},
                           {'subplot': [
                               {'series': cs, 'legend-name': 'Consumer Sentiment'}], 'title': 'Consumer Sentiment'},
                           {'subplot': [
                               {'series': infl, 'legend-name': 'Inflation'}], 'title': 'Inflation'},
                           ], subplot_height=325)

fig.show()

