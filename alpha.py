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
            
            print('----gathering cash flow data for',t)
                        
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
    
    
    def plot_cash_flow(self):
        
        # check to see if the balance sheet data has been pulled for this instance of the object
        # if not get it before continuing
        if not hasattr(self, 'cash_flow'):
            self.get_cashflow()
            
        fig = plt.subplots.make_subplots(rows=2, cols=2, subplot_titles=("Operating Cash Flow",
                                                                         "Cap Ex",
                                                                         'Net Income',
                                                                         'Payments For Repurchase Of CommonStock'))
        
        for st in range(0,len(self.tickers)):
            
            s = self.tickers[st]            
            print(s)
            
            graph_colors = self.graph_colors[0:len(self.tickers)]            
            s_df = self.cash_flow[self.cash_flow['ticker'] == s]
          
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                     y=s_df['operatingCashflow'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=1, col=1)
            
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                     y=s_df['capitalExpenditures'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=1, col=2)
            
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                     y=s_df['netIncome'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=2, col=1)
            
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                     y=s_df['paymentsForRepurchaseOfCommonStock'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=2, col=2)
            
            
        fig.update_layout(showlegend=False,template="plotly_dark")
        fig.show()
        
    
    def plot_short_term_assets(self):
        
        # check to see if the balance sheet data has been pulled for this instance of the object
        # if not get it before continuing
        if not hasattr(self, 'balance_sheets'):
            self.get_balance_sheets()
        
        plt.io.renderers.default='browser' 
        
        fig = plt.subplots.make_subplots(rows=2, cols=2, subplot_titles=("Total Current Assets",
                                                            "Cash and Equivalents",
                                                            "Inventory",
                                                            "Current Net Receivables"))
        
        for st in range(0,len(self.tickers)):
            
            s = self.tickers[st]
            graph_colors = self.graph_colors[0:len(self.tickers)]            
            s_df = self.balance_sheets[self.balance_sheets['ticker'] == s]
          
            
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                     y=s_df['totalCurrentAssets'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=1, col=1)
    
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                     y=s_df['cashAndCashEquivalentsAtCarryingValue'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=1, col=2)
    
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'],
                                     y=s_df['inventory'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=2, col=1)
    
            fig.add_trace(go.Scatter(x=s_df['fiscalDateEnding'], 
                                     y=s_df['currentNetReceivables'],
                                     name=s,
                                     line=dict(color=graph_colors[st])),
                          row=2, col=2)
    
    
        fig.update_layout(showlegend=False,template="plotly_dark")
        fig.show()
        
        
    



#def plot_short_term_assets()
#api_key = '296ULICGSB63VL7A'
#sbs = Stonks(api_key, ['INTC', 'AMD']).get_balance_sheets()
#print(sbs.get_overview().overview['AMD'])
#print(sbs['ticker'])
#sbo = Stonks(api_key,['INTC','AMD']).get_overview()
#print(sbo['AMD'])


