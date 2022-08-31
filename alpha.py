# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:08:21 2022

@author: Korey
"""
import requests
import pandas as pd
import plotly as plt
import plotly.graph_objects as go

class Equities:
    
    # any variables defined here are considered class variables

    # init is a constructor method and is automatically called to allocate memory when a new object/instance
    # is created. All classes have an __init__ method. It helps in distinguising a class variable 
    # from a local variable
    
    # sometime the init method is just referred to as constructor
    def __init__(self, api_key, tickers):
        
        # any variables defined here are considered instance variables
        self.api_key = api_key
        self.tickers = tickers
        self.graph_colors = plt.colors.DEFAULT_PLOTLY_COLORS
        
    
    def alpha_vantage_get(self,function=None,symbol=None):
        
        url = 'https://www.alphavantage.co/query?function='+function+'&symbol='+symbol+'&apikey='+self.api_key
        r = requests.get(url)
        data = r.json()
        
        return data
    
    
    def get_cashflow(self):
                
        # list to store dataframes in
        dfs = []
        
        for t in self.tickers:
            
            print('----gathering cash flow data for',t)
            data = self.alpha_vantage_get(function='CASH_FLOW',symbol=t)
            df = pd.DataFrame.from_dict(data['annualReports'])
            df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric, errors='coerce')
            df['ticker'] = t
            dfs.append(df)
        
        return_df = pd.concat(dfs)
        return_df.set_index('fiscalDateEnding')

        self.cash_flow = return_df

        return return_df
        

    def get_overview(self):
        
        return_dict = {}
        
        for t in self.tickers:
            data = self.alpha_vantage_get(function="OVERVIEW",symbol=t)
            return_dict[t] = data
            
        self.overview = return_dict
            
        return return_dict
        
         
    def get_balance_sheets(self):
        
        # list to store dataframes in
        dfs = []
        
        # for each ticker make a request
        # TODO add timer between requests based on level of alpha vantage API call volume allowed per minute
        for t in self.tickers:   
            
            print('----gathering balance sheet data for',t)
                        
            data = self.alpha_vantage_get(function='BALANCE_SHEET',symbol=t)
            
            # create a dataframe
            # TODO check for empty return
            df = pd.DataFrame.from_dict(data['annualReports'])
            df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric, errors='coerce')
            
            # add symbol as field in dataframe
            df['ticker'] = t
            dfs.append(df)

        return_df = pd.concat(dfs)
        return_df.set_index('fiscalDateEnding')

        self.balance_sheets = return_df

        return return_df
    
    
    def plot_subplots(self,plot_type='cash_flow',columns={}):
        
        df = None
        
        if plot_type == 'cash_flow':
            
            # if we haven't populated cash flow data on this instance of the class
            # go populate
            if not hasattr(self,'cash_flow'):
                self.get_cashflow()
                
            df = self.cash_flow
                
            # if no plot columns were passed use defualt
            if not columns:
                columns={'operatingCashflow':'Operating Cash Flow',
                         'capitalExpenditures':'Cap Ex',
                         'netIncome':'Net Income',
                         'paymentsForRepurchaseOfCommonStock':  'Payments For Repurchase Of CommonStock'}
                
        
        if plot_type == 'balance_sheet':
            
            # if we haven't populated cash flow data on this instance of the class
            # go populate
            if not hasattr(self,'balance_sheets'):
                self.get_balance_sheets()
                
            df = self.balance_sheets
                
            # if no plot columns were passed use defualt
            if not columns:
                columns={'totalCurrentAssets':'Total Current Assets',
                        'cashAndCashEquivalentsAtCarryingValue': 'Cash and Equivalents',
                        'inventory':'Inventory',
                        'currentNetReceivables':'Current Net Recievables',
                        'totalCurrentLiabilities': 'Current Liabilities'}
                
        
                
        plt.io.renderers.default='browser'
        
        # we always do a max of two columns, rows can change based on the number of columns which get passed
        row_count = (len(columns) % 2) + (len(columns) // 2)
        
        # each row gets 300 pixels, this is updated after for loop
        fig_height = row_count * 300
        
        plot_titles = [columns[k] for i,k in enumerate(columns)]
        
        fig = plt.subplots.make_subplots(rows=row_count, cols=2, subplot_titles=plot_titles)
        
        
        
        for index, s in enumerate(self.tickers):            
            graph_colors = self.graph_colors[0:len(self.tickers)]            
            s_df = df[df['ticker'] == s]
            
            for i,k in enumerate(columns,start=1):              
                ## index is starting at 1, increment by 1 then 
                # floor of 2//2 = 1, 3//2=1, 4//2 = 2, 5//2 = 2 and so on
                row_place = (i+1)//2 
                col_place = 1
                
                # we have two columns, place graph on column based on integer even or odd
                if i % 2 != 0:
                    col_place = 1
                else: 
                    col_place = 2
                    
                fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                         y=s_df[k],
                                         name=s,
                                         line=dict(color=graph_colors[index])),
                              row=row_place, col=col_place)
                    
        fig.update_layout(showlegend=False,template="plotly_dark",height=fig_height)
        fig.show()
                
                
        
        
    
        
#----------------TESTING----------------------    
    
stock_symbols = ['AAPL','SHOP','GOOG','NVDA','UAL']

# test balance sheet
equities = Equities(api_key='296ULICGSB63VL7A',tickers=stock_symbols)

equities.plot_subplots(plot_type='cash_flow')
equities.plot_subplots(plot_type='balance_sheet')

#bs = equities.get_balance_sheets()
#print(bs.columns)
#equities.plot_short_term_assets()


#def plot_short_term_assets()
#api_key = '296ULICGSB63VL7A'
#sbs = Stonks(api_key, ['INTC', 'AMD']).get_balance_sheets()
#print(sbs.get_overview().overview['AMD'])
#print(sbs['ticker'])
#sbo = Stonks(api_key,['INTC','AMD']).get_overview()
#print(sbo['AMD'])


