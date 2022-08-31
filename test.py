# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:03:12 2022
@author: Korey
"""

import alpha as a
import pandas as pd
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default='browser'

colors = plotly.colors.DEFAULT_PLOTLY_COLORS

#stock_symbols = ['AMD','INTC','NVDA']
stock_symbols = ['F','TSLA']

# test balance sheet
equities = a.Equities(api_key='296ULICGSB63VL7A',tickers=stock_symbols)

bs = equities.get_balance_sheets()
print(bs.columns)
equities.plot_short_term_assets()

# test cash flow
#cf_df = equities.get_cashflow()
#print(cf_df.columns)
#equities.plot_cash_flow()

'''
cf = equities.get_cashflow()
print(cf.columns)
print(cf['operatingCashflow'])
fig = px.line(cf,x="fiscalDateEnding",y='operatingCashflow',color='ticker')
fig.show()
'''
