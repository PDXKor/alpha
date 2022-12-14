# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:01:02 2022

@author: Korey
"""

from alpha import core_api as a
from alpha import subplots


# pass in your own api_key
api_key = '296ULICGSB63VL7A' 

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
fig = subplots.build_subplots(data=[{'subplot': [{'series': ty_ten,
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

